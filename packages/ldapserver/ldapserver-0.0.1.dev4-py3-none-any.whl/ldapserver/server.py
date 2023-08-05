import traceback
import ssl
import socketserver
import typing

from . import asn1, exceptions, ldap, schema

def reject_critical_controls(controls=None):
	for control in controls or []:
		if control.criticality:
			raise exceptions.LDAPUnavailableCriticalExtension()

class BaseLDAPRequestHandler(socketserver.BaseRequestHandler):
	def setup(self):
		super().setup()
		self.keep_running = True

	def handle(self):
		buf = b''
		while self.keep_running:
			try:
				shallowmsg, buf = ldap.ShallowLDAPMessage.from_ber(buf)
				for respmsg in self.handle_message(shallowmsg):
					self.request.sendall(ldap.LDAPMessage.to_ber(respmsg))
			except asn1.IncompleteBERError:
				chunk = self.request.recv(4096)
				if not chunk:
					self.keep_running = False
					self.request.close()
				else:
					buf += chunk
		self.request.close()

	def handle_message(self, shallowmsg: ldap.ShallowLDAPMessage) -> typing.Iterable[ldap.LDAPMessage]:
		'''Handle an LDAP request foobar

		:param shallowmsg: Half-decoded LDAP message to handle
		:returns: Response messages
		'''
		msgtypes = {
			ldap.BindRequest: (self.handle_bind, ldap.BindResponse),
			ldap.UnbindRequest: (self.handle_unbind, None),
			ldap.SearchRequest: (self.handle_search, ldap.SearchResultDone),
			ldap.ModifyRequest: (self.handle_modify, ldap.ModifyResponse),
			ldap.AddRequest: (self.handle_add,  ldap.AddResponse),
			ldap.DelRequest: (self.handle_delete, ldap.DelResponse),
			ldap.ModifyDNRequest: (self.handle_modifydn, ldap.ModifyDNResponse),
			ldap.CompareRequest: (self.handle_compare, ldap.CompareResponse),
			ldap.AbandonRequest: (self.handle_abandon, None),
			ldap.ExtendedRequest: (self.handle_extended, ldap.ExtendedResponse),
		}
		handler, response_type = msgtypes.get(shallowmsg.protocolOpType, (None, None))
		try:
			if handler is None:
				raise exceptions.LDAPProtocolError()
			try:
				msg = shallowmsg.decode()[0]
			except ValueError as e:
				self.on_recv_invalid(shallowmsg)
				raise exceptions.LDAPProtocolError() from e
			for args in handler(msg.protocolOp, msg.controls):
				response, controls = args if isinstance(args, tuple) else (args, None)
				yield ldap.LDAPMessage(shallowmsg.messageID, response, controls)
		except exceptions.LDAPError as e:
			if response_type is not None:
				respmsg = ldap.LDAPMessage(shallowmsg.messageID, response_type(e.code, diagnosticMessage=e.message))
				yield respmsg
		except Exception as e: # pylint: disable=broad-except
			if response_type is not None:
				respmsg = ldap.LDAPMessage(shallowmsg.messageID, response_type(ldap.LDAPResultCode.other))
				yield respmsg
			self.on_exception(e)

	def on_recv_invalid(self, shallowmsg):
		pass

	def on_exception(self, e):
		traceback.print_exc()

	def handle_bind(self, op: ldap.BindRequest, controls=None) -> typing.Iterable[ldap.ProtocolOp]:
		reject_critical_controls(controls)
		raise exceptions.LDAPAuthMethodNotSupported()

	def handle_unbind(self, op: ldap.UnbindRequest, controls=None) -> typing.NoReturn:
		reject_critical_controls(controls)
		self.keep_running = False

	def handle_search(self, op: ldap.SearchRequest, controls=None) -> typing.Iterable[ldap.ProtocolOp]:
		reject_critical_controls(controls)
		yield ldap.SearchResultDone(ldap.LDAPResultCode.success)

	def handle_modify(self, op: ldap.ModifyRequest, controls=None) -> typing.Iterable[ldap.ProtocolOp]:
		reject_critical_controls(controls)
		raise exceptions.LDAPInsufficientAccessRights()

	def handle_add(self, op: ldap.AddRequest, controls=None) -> typing.Iterable[ldap.ProtocolOp]:
		reject_critical_controls(controls)
		raise exceptions.LDAPInsufficientAccessRights()

	def handle_delete(self, op: ldap.DelRequest, controls=None) -> typing.Iterable[ldap.ProtocolOp]:
		reject_critical_controls(controls)
		raise exceptions.LDAPInsufficientAccessRights()

	def handle_modifydn(self, op: ldap.ModifyDNRequest, controls=None) -> typing.Iterable[ldap.ProtocolOp]:
		reject_critical_controls(controls)
		raise exceptions.LDAPInsufficientAccessRights()

	def handle_compare(self, op: ldap.CompareRequest, controls=None) -> typing.Iterable[ldap.ProtocolOp]:
		reject_critical_controls(controls)
		raise exceptions.LDAPInsufficientAccessRights()

	def handle_abandon(self, op: ldap.AbandonRequest, controls=None) -> typing.NoReturn:
		reject_critical_controls(controls)

	def handle_extended(self, op: ldap.ExtendedRequest, controls=None) -> typing.Iterable[ldap.ProtocolOp]:
		reject_critical_controls(controls)
		raise exceptions.LDAPProtocolError()

class LDAPRequestHandler(BaseLDAPRequestHandler):
	'''
	.. py:attribute:: rootdse

		Special :any:`LDAPObject` that contains information
		about the server, such as supported extentions and SASL authentication
		mechansims. Attributes can be accessed in a dict-like fashion.
	'''

	subschema = schema.RFC4519_SUBSCHEMA
	'''
	.. py:attribute:: subschema

		Special :any:`LDAPObject` that describes the schema.
		Per default the subschema includes standard syntaxes, standard matching
		rules and objectclasses/attributetypes for the rootdse and subschema.
		It does not include objectclasses/attributetypes for actual data
		(e.g. users and groups). See :any:`Subschema` for details.

		If `subschema` is not `None`, the subschemaSubentry attribute is
		automatically added to all results returned by :any:`do_search`.
	'''

	static_objects = tuple()

	def setup(self):
		super().setup()
		self.rootdse = self.subschema.RootDSE()
		self.rootdse['objectClass'] = ['top']
		self.rootdse['supportedSASLMechanisms'] = self.get_sasl_mechanisms
		self.rootdse['supportedExtension'] = self.get_extentions
		self.rootdse['supportedLDAPVersion'] = ['3']
		self.bind_object = None
		self.bind_sasl_state = None

	def get_extentions(self):
		'''Get supported LDAP extentions

		:returns: OIDs of supported LDAP extentions
		:rtype: list of bytes objects

		Called whenever the root DSE attribute "supportedExtension" is queried.'''
		res = []
		if self.supports_starttls:
			res.append(ldap.EXT_STARTTLS_OID)
		if self.supports_whoami:
			res.append(ldap.EXT_WHOAMI_OID)
		if self.supports_password_modify:
			res.append(ldap.EXT_PASSWORD_MODIFY_OID)
		return res

	def get_sasl_mechanisms(self):
		'''Get supported SASL mechanisms

		:returns: Names of supported SASL mechanisms
		:rtype: list of bytes objects

		SASL mechanism name are typically all-caps, like "EXTERNAL".

		Called whenever the root DSE attribute "supportedSASLMechanisms" is queried.'''
		res = []
		if self.supports_sasl_anonymous:
			res.append('ANONYMOUS')
		if self.supports_sasl_plain:
			res.append('PLAIN')
		if self.supports_sasl_external:
			res.append('EXTERNAL')
		return res

	def handle_bind(self, op, controls=None):
		reject_critical_controls(controls)
		if op.version != 3:
			raise exceptions.LDAPProtocolError('Unsupported protocol version')
		auth = op.authentication
		# Resume ongoing SASL dialog
		if self.bind_sasl_state and isinstance(auth, ldap.SaslCredentials) \
				and auth.mechanism == self.bind_sasl_state[0]:
			mechanism, iterator = self.bind_sasl_state
			self.bind_sasl_state = None
			resp_code = ldap.LDAPResultCode.saslBindInProgress
			try:
				resp = iterator.send(auth.credentials)
				self.bind_sasl_state = (mechanism, iterator)
			except StopIteration as e:
				resp_code = ldap.LDAPResultCode.success
				self.bind_object, resp = e.value # pylint: disable=unpacking-non-sequence
			yield ldap.BindResponse(resp_code, serverSaslCreds=resp)
			return
		# If auth type or SASL method changed, abort SASL dialog
		self.bind_sasl_state = None
		if isinstance(auth, ldap.SimpleAuthentication):
			self.bind_object = self.do_bind_simple(op.name, auth.password)
			yield ldap.BindResponse(ldap.LDAPResultCode.success)
		elif isinstance(auth, ldap.SaslCredentials):
			ret = self.do_bind_sasl(auth.mechanism, auth.credentials)
			if isinstance(ret, tuple):
				self.bind_object, resp = ret
				yield ldap.BindResponse(ldap.LDAPResultCode.success, serverSaslCreds=resp)
				return
			iterator = iter(ret)
			resp_code = ldap.LDAPResultCode.saslBindInProgress
			try:
				resp = next(iterator)
				self.bind_sasl_state = (auth.mechanism, iterator)
			except StopIteration as e:
				resp_code = ldap.LDAPResultCode.success
				self.bind_object, resp = e.value # pylint: disable=unpacking-non-sequence
			yield ldap.BindResponse(resp_code, serverSaslCreds=resp)
		else:
			yield from super().handle_bind(op, controls) # pylint: disable=not-an-iterable

	def do_bind_simple(self, dn='', password=b''):
		'''Do LDAP BIND with simple authentication

		:param dn: Distinguished name of object to be authenticated or empty
		:type dn: str
		:param password: Password, may be empty
		:type password: bytes

		:returns: Bind object
		:rtype: obj

		Delegates implementation to :any:`do_bind_simple_anonymous`,
		:any:`do_bind_simple_unauthenticated` or :any:`do_bind_simple_authenticated`
		according to `RFC 4513`_.'''
		if not dn and not password:
			return self.do_bind_simple_anonymous()
		if not password:
			return self.do_bind_simple_unauthenticated(dn)
		return self.do_bind_simple_authenticated(dn, password)

	def do_bind_simple_anonymous(self):
		'''Do LDAP BIND with simple anonymous authentication (`RFC 4513 5.1.1.`_)

		:raises exceptions.LDAPError: if authentication failed

		:returns: Bind object on success
		:rtype: obj

		Calld by :any:`do_bind_simple`. Always returns None.'''
		return None

	def do_bind_simple_unauthenticated(self, dn):
		'''Do LDAP BIND with simple unauthenticated authentication (`RFC 4513 5.1.2.`_)

		:param dn: Distinguished name of the object to be authenticated
		:type dn: str

		:raises exceptions.LDAPError: if authentication failed

		:returns: Bind object on success
		:rtype: obj

		Calld by :any:`do_bind_simple`. The default implementation always raises an
		:any:`LDAPInvalidCredentials` exception.'''
		raise exceptions.LDAPInvalidCredentials()

	def do_bind_simple_authenticated(self, dn, password):
		'''Do LDAP BIND with simple name/password authentication (`RFC 4513 5.1.3.`_)

		:param dn: Distinguished name of the object to be authenticated
		:type dn: str
		:param password: Password for object
		:type dn: bytes

		:raises exceptions.LDAPError: if authentication failed

		:returns: Bind object on success
		:rtype: obj

		Calld by :any:`do_bind_simple`. The default implementation always raises an
		`LDAPInvalidCredentials` exception.'''
		raise exceptions.LDAPInvalidCredentials()

	def do_bind_sasl(self, mechanism, credentials=None, dn=None):
		'''Do LDAP BIND with SASL authentication (RFC 4513 and 4422)

		:param mechanism: Name of the selected SASL mechanism
		:type mechanism: str
		:param credentials: Initial client response
		:type credentials: bytes, optional
		:param dn: Distinguished name in LDAP BIND request, should be ignored for
		           SASL authentication
		:type dn: str, optional

		:returns: Bind object and final server challenge, only returns on success
		:rtype: Tuple (obj, bytes/None)

		The call only returns if authentication succeeded. In any other case,
		an appropriate :any:`exceptions.LDAPError` is raised.

		Some SASL methods require additional challenge-response round trips. These
		can be achieved with the `yield` statement:

		    client_response = yield server_challenge

		Generally all server challenges and client responses can always be absent
		(indicated by None), empty (empty bytes object) or consist of any number
		of bytes. Whether a challenge or response may or must be absent or present
		is defined by the individual SASL mechanism.

		IANA list of SASL mechansims: https://www.iana.org/assignments/sasl-mechanisms/sasl-mechanisms.xhtml
		'''
		if not mechanism:
			# Request to abort current negotiation (RFC4513 5.2.1.2)
			raise exceptions.LDAPAuthMethodNotSupported()
		if mechanism == 'ANONYMOUS' and self.supports_sasl_anonymous:
			if credentials is not None:
				credentials = credentials.decode()
			return self.do_bind_sasl_anonymous(trace_info=credentials), None
		if mechanism == 'PLAIN' and self.supports_sasl_plain:
			if credentials is None:
				raise exceptions.LDAPProtocolError('Unsupported protocol version')
			authzid, authcid, password = credentials.split(b'\0', 2)
			return self.do_bind_sasl_plain(authcid.decode(), password.decode(), authzid.decode() or None), None
		if mechanism == 'EXTERNAL' and self.supports_sasl_external:
			if credentials is not None:
				credentials = credentials.decode()
			return self.do_bind_sasl_external(authzid=credentials), None
		raise exceptions.LDAPAuthMethodNotSupported()

	supports_sasl_anonymous = False

	def do_bind_sasl_anonymous(self, trace_info=None):
		'''Do LDAP BIND with SASL "ANONYMOUS" mechanism (RFC 4505)

		:param trace_info: Trace information, either an email address or an
		                   opaque string that does not contain the '@' character
		:type trace_info: str, optional

		:raises exceptions.LDAPError: if authentication failed

		:returns: Bind object on success
		:rtype: obj

		Calld by :any:`do_bind_sasl`. The default implementation raises an
		:any:`LDAPAuthMethodNotSupported` exception.'''
		raise exceptions.LDAPAuthMethodNotSupported()

	supports_sasl_plain = False

	def do_bind_sasl_plain(self, identity, password, authzid=None):
		'''Do LDAP BIND with SASL "PLAIN" mechanism (RFC 4616)

		:param identity: Authentication identity (authcid)
		:type identity: str
		:param password: Password (passwd)
		:type password: str
		:param authzid: Authorization identity
		:type authzid: str, optional

		:raises exceptions.LDAPError: if authentication failed

		:returns: Bind object on success
		:rtype: obj

		Calld by :any:`do_bind_sasl`. The default implementation raises an
		:any:`LDAPAuthMethodNotSupported` exception.'''
		raise exceptions.LDAPAuthMethodNotSupported()

	supports_sasl_external = False

	def do_bind_sasl_external(self, authzid=None):
		'''Do LDAP BIND with SASL "EXTERNAL" mechanism (RFC 4422 and 4513)

		:param authzid: Authorization identity
		:type authzid: str, optional

		:raises exceptions.LDAPError: if authentication failed

		:returns: Bind object on success
		:rtype: obj

		EXTERNAL is commonly used for TLS client certificate authentication or
		system user based authentication on UNIX sockets.

		Calld by :any:`do_bind_sasl`. The default implementation raises an
		:any:`LDAPAuthMethodNotSupported` exception.'''
		raise exceptions.LDAPAuthMethodNotSupported()

	def handle_search(self, op, controls=None):
		reject_critical_controls(controls)
		for obj in self.do_search(op.baseObject, op.scope, op.filter):
			if obj.match_search(op.baseObject, op.scope, op.filter):
				yield obj.get_search_result_entry(op.attributes, op.typesOnly)
		yield ldap.SearchResultDone(ldap.LDAPResultCode.success)

	def do_search(self, baseobj, scope, filterobj):
		'''Do LDAP SEARCH operation

		:param baseobj: Distinguished name of the LDAP entry relative to which the
		                search is to be performed
		:type baseobj: str
		:param scope: Search scope
		:type scope: SearchScope
		:param filterobj: Filter object
		:type filterobj: Filter

		:raises exceptions.LDAPError: on error

		:returns: Iterable of dn, attributes tuples

		The default implementation returns matching objects from the root dse and
		the subschema.'''
		yield self.rootdse
		yield self.subschema
		yield from self.static_objects

	def handle_unbind(self, op, controls=None):
		reject_critical_controls(controls)
		self.keep_running = False
		return []

	def handle_extended(self, op, controls=None):
		reject_critical_controls(controls)
		if op.requestName == ldap.EXT_STARTTLS_OID and self.supports_starttls:
			# StartTLS (RFC 4511)
			yield ldap.ExtendedResponse(ldap.LDAPResultCode.success, responseName=ldap.EXT_STARTTLS_OID)
			try:
				self.do_starttls()
			except Exception: # pylint: disable=broad-except
				traceback.print_exc()
				self.keep_running = False
		elif op.requestName == ldap.EXT_WHOAMI_OID and self.supports_whoami:
			# "Who am I?" Operation (RFC 4532)
			identity = (self.do_whoami() or '').encode()
			yield ldap.ExtendedResponse(ldap.LDAPResultCode.success, responseValue=identity)
		elif op.requestName == ldap.EXT_PASSWORD_MODIFY_OID and self.supports_password_modify:
			# Password Modify Extended Operation (RFC 3062)
			newpw = None
			if op.requestValue is None:
				newpw = self.do_password_modify()
			else:
				decoded, _ = ldap.PasswdModifyRequestValue.from_ber(op.requestValue)
				# pylint: disable=no-member
				newpw = self.do_password_modify(decoded.userIdentity, decoded.oldPasswd, decoded.newPasswd)
			if newpw is None:
				yield ldap.ExtendedResponse(ldap.LDAPResultCode.success)
			else:
				encoded = ldap.PasswdModifyResponseValue.to_ber(ldap.PasswdModifyResponseValue(newpw))
				yield ldap.ExtendedResponse(ldap.LDAPResultCode.success, responseValue=encoded)
		else:
			yield from super().handle_extended(op, controls) # pylint: disable=not-an-iterable

	#: :any:`ssl.SSLContext` for StartTLS
	ssl_context = None

	@property
	def supports_starttls(self):
		'''
		'''
		return self.ssl_context is not None and not isinstance(self.request, ssl.SSLSocket)

	def do_starttls(self):
		'''Do StartTLS extended operation (RFC 4511)

		Called by `handle_extended()` if :any:`supports_starttls` is True. The default
		implementation uses `ssl_context`.

		Note that the (success) response to the request is sent before this method
		is called. If a call to this method fails, the LDAP connection is
		immediately terminated.'''
		self.request = self.ssl_context.wrap_socket(self.request, server_side=True)

	#:
	supports_whoami = False

	def do_whoami(self):
		'''Do "Who am I?" extended operation (RFC 4532)

		:returns: Current authorization identity (authzid) or empty string for anonymous sessions
		:rtype: str

		Called by `handle_extended()` if `supports_whoami` is True. The default
		implementation always returns an empty string.'''
		return ''

	#:
	supports_password_modify = False

	def do_password_modify(self, user=None, old_password=None, new_password=None):
		'''Do password modify extended operation (RFC 3062)

		:param user: User the request relates to, may or may not be a
		             distinguished name. If absent, the request relates to the
		             user currently associated with the LDAP connection
		:type user: str, optional
		:param old_password: Current password of user
		:type old_password: bytes, optional
		:param new_password: Desired password for user
		:type new_password: bytes, optional

		Called by `handle_extended()` if :any:`supports_password_modify` is True. The
		default implementation always raises an :any:`LDAPUnwillingToPerform` error.'''
		raise exceptions.LDAPUnwillingToPerform()
