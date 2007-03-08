
# Single Sign-On Authentication method (used by MSNP15+)
snit::type SSOAuthentication {
	variable authenticationTicket ""
	variable voiceTicket ""
	variable spacesTicket ""
	variable contactTicket ""
	variable websiteTicket ""

	method Authenticate { callback url } { 
		error "UNSUPPORTED"
	}
}

snit::type TWNAuthentication {
	variable messengerTicket ""
	variable voiceTicket ""
	variable contactsTicket ""

	variable MESSENGER_URL "messenger.msn.com"
	variable VOICE_URL "voice.messenger.msn.com"
	variable CONTACTS_URL "contacts.messenger.msn.com"

	method Authenticate { callback url } {
		return [$self AuthenticatePassport3 $callback $url]
	}
	method GetMessengerTicket { } {
		return $messengerTicket
	}

	method AuthenticatePassport3Error { callbk msg } {
		if {[catch {eval $callbk [list 2]} result]} {
			bgerror $result
		}
	}
	
	method AuthenticatePassport3Callback { callbk soap_req data } {
		set xml [SOAP::dump $soap_req]
		set list [xml2list $xml]
		
		if { [GetXmlNode $list "S:Envelope:S:Fault"] != "" } {
			# TODO find a way to specify if it's a wrong password or a server error..
			set faultcode [GetXmlEntry $list "S:Envelope:S:Fault:faultcode"]	;# Should be "wsse:FailedAuthentication"
			set faultstring [GetXmlEntry $list "S:Envelope:S:Fault:faultstring"]
			
			if {[catch {eval $callbk [list 1]} result]} {
				bgerror $result
			}	
		}
		set i 0
		while {1 } {
			set subxml [GetXmlNode $list "S:Envelope:S:Body:wst:RequestSecurityTokenResponseCollection:wst:RequestSecurityTokenResponse" $i]
			incr i
			if  { $subxml == "" } {
				break
			}
			
			set type [GetXmlEntry $subxml "wst:RequestSecurityTokenResponse:wsp:AppliesTo:wsa:EndpointReference:wsa:Address"]
			if { $type == $MESSENGER_URL } {
				set messengerTicket [GetXmlEntry $subxml "wst:RequestSecurityTokenResponse:wst:RequestedSecurityToken:wsse:BinarySecurityToken"]
			} elseif { $type == $VOICE_URL } {
				set voiceTicket [GetXmlEntry $subxml "wst:RequestSecurityTokenResponse:wst:RequestedSecurityToken:wsse:BinarySecurityToken"]
			} elseif { $type == $CONTACTS_URL } {
				set contactsTicket [GetXmlEntry $subxml "wst:RequestSecurityTokenResponse:wst:RequestedSecurityToken:wsse:BinarySecurityToken"]
			}
		
		}
		if {[catch {eval $callbk [list 0]} result]} {
			bgerror $result
		}
	}
	
	method AuthenticatePassport3 { callbk url } {
		set soap_req [SOAP::create AuthenticatePassport3 \
				  -uri "https://loginnet.passport.com/RST.srf" \
				  -proxy "https://loginnet.passport.com/RST.srf" \
				  -wrapProc [list $self getPassport3Xml $url] \
				  -errorCommand [list $self AuthenticatePassport3Error $callbk]]
		SOAP::configure AuthenticatePassport3 -command [list $self AuthenticatePassport3Callback $callbk $soap_req]
		$soap_req

		return ""
	}
	
	method getPassport3Xml { url args } {
		# TODO make login and password as options!
		
		set xml {<?xml version="1.0" encoding="UTF-8"?><Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wsse="http://schemas.xmlsoap.org/ws/2003/06/secext" xmlns:saml="urn:oasis:names:tc:SAML:1.0:assertion" xmlns:wsp="http://schemas.xmlsoap.org/ws/2002/12/policy" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd" xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/03/addressing" xmlns:wssc="http://schemas.xmlsoap.org/ws/2004/04/sc" xmlns:wst="http://schemas.xmlsoap.org/ws/2004/04/trust"><Header><ps:AuthInfo xmlns:ps="http://schemas.microsoft.com/Passport/SoapServices/PPCRL" Id="PPAuthInfo"><ps:HostingApp>{7108E71A-9926-4FCB-BCC9-9A9D3F32E423}</ps:HostingApp><ps:BinaryVersion>4</ps:BinaryVersion><ps:UIVersion>1</ps:UIVersion><ps:Cookies></ps:Cookies><ps:RequestParams>AQAAAAIAAABsYwQAAAAzMDg0</ps:RequestParams></ps:AuthInfo><wsse:Security><wsse:UsernameToken Id="user"><wsse:Username>}
		append xml [config::getKey login]
		append xml {</wsse:Username><wsse:Password>}
		append xml $::password
		append xml {</wsse:Password></wsse:UsernameToken></wsse:Security></Header><Body><ps:RequestMultipleSecurityTokens xmlns:ps="http://schemas.microsoft.com/Passport/SoapServices/PPCRL" Id="RSTS"><wst:RequestSecurityToken Id="RST0"><wst:RequestType>http://schemas.xmlsoap.org/ws/2004/04/security/trust/Issue</wst:RequestType><wsp:AppliesTo><wsa:EndpointReference><wsa:Address>http://Passport.NET/tb</wsa:Address></wsa:EndpointReference></wsp:AppliesTo></wst:RequestSecurityToken><wst:RequestSecurityToken Id="RST1"><wst:RequestType>http://schemas.xmlsoap.org/ws/2004/04/security/trust/Issue</wst:RequestType><wsp:AppliesTo><wsa:EndpointReference><wsa:Address>messenger.msn.com</wsa:Address></wsa:EndpointReference></wsp:AppliesTo><wsse:PolicyReference URI=}
		append xml "\"?[string map { "," "&amp;" } [urldecode $url]]\""
		append xml {></wsse:PolicyReference></wst:RequestSecurityToken><wst:RequestSecurityToken Id="RST2"><wst:RequestType>http://schemas.xmlsoap.org/ws/2004/04/security/trust/Issue</wst:RequestType><wsp:AppliesTo><wsa:EndpointReference><wsa:Address>contacts.msn.com</wsa:Address></wsa:EndpointReference></wsp:AppliesTo><wsse:PolicyReference URI="?cb=&amp;fs=1&amp;id=24000&amp;kv=9&amp;rn=UFkjwrlz&amp;tw=43200&amp;ver=2.1.6000.1"></wsse:PolicyReference></wst:RequestSecurityToken><wst:RequestSecurityToken Id="RST3"><wst:RequestType>http://schemas.xmlsoap.org/ws/2004/04/security/trust/Issue</wst:RequestType><wsp:AppliesTo><wsa:EndpointReference><wsa:Address>voice.messenger.msn.com</wsa:Address></wsa:EndpointReference></wsp:AppliesTo><wsse:PolicyReference URI="?id=69264"></wsse:PolicyReference></wst:RequestSecurityToken></ps:RequestMultipleSecurityTokens></Body></Envelope>}
		return $xml
	}
}


snit::type LockKeyAuthentication {
	

	method CreateLockKey {chldata prodid prodkey} {
        
                # Create an MD5 hash out of the given data, then form 32 bit integers from it
                set md5hash [::md5::md5 $chldata$prodkey]
                set md5parts [$self MD5HashToInt $md5hash]
        

                # Then create a valid productid string, divisable by 8, then form 32 bit integers from it
                set nrPadZeros [expr {8 - [string length $chldata$prodid] % 8}]
                set padZeros [string repeat 0 $nrPadZeros]
                set chlprodid [$self CHLProdToInt $chldata$prodid$padZeros]

                # Create the key we need to XOR
                set key [$self KeyFromInt $md5parts $chlprodid]

                set low 0x[string range $md5hash 0 15]
                set high 0x[string range $md5hash 16 32]
                set low [expr {$low ^ $key}]
                set high [expr {$high ^ $key}]

                set p1 [format %8.8x [expr {($low / 0x100000000) % 0x100000000}]]
                set p2 [format %8.8x [expr {$low % 0x100000000}]]
                set p3 [format %8.8x [expr {($high / 0x100000000) % 0x100000000}]]
                set p4 [format %8.8x [expr {$high % 0x100000000}]]

                return $p1$p2$p3$p4
        }

        method KeyFromInt { md5parts chlprod } {
                # Create a new series of numbers
                set key_temp 0
                set key_high 0
                set key_low 0
        
                # Then loop on the entries in the second array we got in the parameters
                for {set i 0} {$i < [llength $chlprod]} {incr i 2} {

                        # Make $key_temp zero again and perform calculation as described in the documents
                        set key_temp [lindex $chlprod $i]
                        set key_temp [expr {(wide(0x0E79A9C1) * wide($key_temp)) % wide(0x7FFFFFFF)}]
                        set key_temp [expr {wide($key_temp) + wide($key_high)}]
                        set key_temp [expr {(wide([lindex $md5parts 0]) * wide($key_temp)) + wide([lindex $md5parts 1])}]
                        set key_temp [expr {wide($key_temp) % wide(0x7FFFFFFF)}]

                        set key_high [lindex $chlprod [expr {$i+1}]]
                        set key_high [expr {(wide($key_high) + wide($key_temp)) % wide(0x7FFFFFFF)}]
                        set key_high [expr {(wide([lindex $md5parts 2]) * wide($key_high)) + wide([lindex $md5parts 3])}]
                        set key_high [expr {wide($key_high) % wide(0x7FFFFFFF)}]

                        set key_low [expr {wide($key_low) + wide($key_temp) + wide($key_high)}]
                }

                set key_high [expr {(wide($key_high) + wide([lindex $md5parts 1])) % wide(0x7FFFFFFF)}]
                set key_low [expr {(wide($key_low) + wide([lindex $md5parts 3])) % wide(0x7FFFFFFF)}]

                set key_high 0x[$self byteInvert [format %8.8X $key_high]]
                set key_low 0x[$self byteInvert [format %8.8X $key_low]]

                set long_key [expr {(wide($key_high) << 32) + wide($key_low)}]

                return $long_key
        }

        # Takes an CHLData + ProdID + Padded string and chops it in 4 bytes. Then converts to 32 bit integers 
        method CHLProdToInt { CHLProd } {
                set hexs {}
                set result {}
                while {[string length $CHLProd] > 0} {
                        lappend hexs [string range $CHLProd 0 3]
                        set CHLProd [string range $CHLProd 4 end]
                }
                for {set i 0} {$i < [llength $hexs]} {incr i} {
                        binary scan [lindex $hexs $i] H8 int
                        lappend result 0x[$self byteInvert $int]
                }
                return $result
        }
                

        # Takes an MD5 string and chops it in 4. Then "decodes" the HEX and converts to 32 bit integers. After that it ANDs
        method MD5HashToInt { md5hash } {
                binary scan $md5hash a8a8a8a8 hash1 hash2 hash3 hash4
                set hash1 [expr {"0x[$self byteInvert $hash1]" & 0x7FFFFFFF}]
                set hash2 [expr {"0x[$self byteInvert $hash2]" & 0x7FFFFFFF}]
                set hash3 [expr {"0x[$self byteInvert $hash3]" & 0x7FFFFFFF}]
                set hash4 [expr {"0x[$self byteInvert $hash4]" & 0x7FFFFFFF}]
                
                return [list $hash1 $hash2 $hash3 $hash4]
        }

        method byteInvert { hex } {
                set hexs {}
                while {[string length $hex] > 0} {
                        lappend hexs [string range $hex 0 1]
                        set hex [string range $hex 2 end]
                }
                set hex ""
                for {set i [expr [llength $hexs] -1]} {$i >= 0} {incr i -1} {
                        append hex [lindex $hexs $i]
                }
                return $hex
        }

}

