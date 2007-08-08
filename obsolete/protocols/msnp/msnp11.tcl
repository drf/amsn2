snit::type MSNP11 {
	option -msnp -default ""
	option -account_manager -default ""
	option -protocol -default "" -configuremethod ProtocolOptionChanged
	variable protocol

	variable commandManager 
	variable authenticator ""
	variable group_count 0
	variable user_count 0
	variable group_total 0
	variable user_total 0
	variable last_lst_user ""

	variable keep_alive_id ""

	variable AUTHENTICATION_METHOD "TWN"

	# TODO set the client version to a real client that uses MSNP12
	variable CLIENT_VERSION "8.0.0812"
	variable PRODUCT_KEY "YMM8C_H7KCQ2S_KL"
	variable PRODUCT_ID "PROD0090YUAUV\{2B"


	variable BLP_COMMAND "BLP"
	variable GTC_COMMAND "GTC"
	variable LSG_COMMAND "LSG"
	variable LST_COMMAND "LST"
	variable MSG_COMMAND "MSG" ;# TODO
	variable PRP_COMMAND "PRP"
	variable BPR_COMMAND "BPR"
	variable SBP_COMMAND "SBP"
	variable SBS_COMMAND "SBS"
	variable CHL_COMMAND "CHL"
	variable FLN_COMMAND "FLN"
	variable NLN_COMMAND "NLN"
	variable RNG_COMMAND "RNG" ;# TODO
	variable UBX_COMMAND "UBX" 
	variable UUX_COMMAND "UUX" ;# TODO
	variable IPG_COMMAND "IPG" ;# TODO

	variable USR_COMMAND "USR"
	variable ILN_COMMAND "ILN"
	variable ADC_COMMAND "ADC" ;# TODO
	variable ADG_COMMAND "ADG" ;# TODO
	variable GCF_COMMAND "GCF"
	variable SYN_COMMAND "SYN"
	variable REG_COMMAND "REG" ;# TODO
	variable REM_COMMAND "REM" ;# TODO
	variable RMG_COMMAND "RMG" ;# TODO
	variable XFR_COMMAND "XFR" ;# TODO
	
	variable CHG_COMMAND "CHG"
	variable PNG_COMMAND "PNG"
	variable QNG_COMMAND "QNG"

	variable QRY_COMMAND "QRY"
	variable OUT_COMMAND "OUT"

	variable ONLINE "NLN"
	variable AWAY "AWY"
	variable IDLE "IDL"
	variable BUSY "BSY"
	variable OFFLINE "FLN"
	variable HIDDEN "HDN"
	variable BRB "BRB"
	variable PHONE "PHN"
	variable LUNCH "LUN"

	variable FORWARD_LIST "FL"
	variable ALLOW_LIST "AL"
	variable BLOCK_LIST "BL"
	variable REVERSE_LIST "RL"
	variable PENDING_LIST "PL"

	variable FORWARD_LIST_FLAG_BIT 1
	variable ALLOW_LIST_FLAG_BIT 2
	variable BLOCK_LIST_FLAG_BIT 4
	variable REVERSE_LIST_FLAG_BIT 8
	variable PENDING_LIST_FLAG_BIT 16

	constructor { args } {
		set options(-protocol) [set protocol $self]
		$self configurelist $args		
	}

	destructor {
		after cancel $keep_alive_id
		if {$authenticator != "" } {
			$authenticator destroy
			set authenticator ""
		}
	}

	method ProtocolOptionChanged {option value} {
		set options($option) $value
		if {$options(-protocol) == "" } {
			set options(-protocol) $self
		}
		set protocol $options(-protocol)
	}


	method urldecode {str} {
		set str [split $str "%"]
		set decode [lindex $str 0]

		for {set i 1 } { $i < [llength $str] } { incr i } {
			set char [string range [lindex $str $i] 0 1]
			if { [catch {append decode [binary format H2 $char]}] } {
				append decode "%$char"
			}
			append decode [string range [lindex $str $i] 2 end]
		}
		return [encoding convertfrom utf-8 $decode]
	}

	method urlencode {str} {
		set encode ""

		set utfstr [encoding convertto utf-8 $str]

		for {set i 0} {$i<[string length $utfstr]} {incr i} {
			set character [string range $utfstr $i $i]
			
			if {![string match {[^a-zA-Z0-9()]} $character]} {
				binary scan $character H2 charval
				append encode "%$charval"
			} else {
				append encode "${character}"
			}
		}

		return $encode
	}



	method Logout {  } {
		# We send the logout command and the MSNP object will take care of doing the proper logout code
		# once the socket gets closed by the server... 
		set command [Command create %AUTO% -command $OUT_COMMAND]
		$protocol SendCommand $command
		$command destroy
	}

	method GetLogin { } {
		$options(-msnp) cget -login
	}

	method GetClientId { } {
		# TODO build clientid depending on configured capabilities
		return [::config::getKey clientid]
	}

	method SendCommand { command } {
		$options(-msnp) SendCommand $command
	}

	method SendEvent { event args} {
		# Send event to the account manager..
		eval [linsert $args 0 $options(-msnp) SendEvent $event ]
	}
	
	method getDataManager { } {
		return [$options(-msnp) getDataManager]
	}

	method Authenticate { } {
		set command [$commandManager CreateCommand [list $protocol handleUSR] 1 $USR_COMMAND [$protocol GetAuthenticationMethod] "I" [$protocol GetLogin]]
		$protocol SendCommand $command
		$command destroy
	}

	method GetAuthenticationMethod {} {
		return $AUTHENTICATION_METHOD
	}

	method GetClientVersion { } {
		return $CLIENT_VERSION
	}

	method AuthenticationCompleted { hasError } {
		if {$hasError == 0}  {
			# We send the auth ticket, no need to send the event for Authenticated until we receive the USR OK

			set command [$commandManager CreateCommand [list $protocol handleUSR] 1 $USR_COMMAND [$protocol GetAuthenticationMethod] "S" [$authenticator GetMessengerTicket]]
			$protocol SendCommand $command
			$command destroy
		} else {
			if {$hasError == 1 } {
				# Send the event about the authentication failed
				$protocol SendEvent AuthenticationFailed 
			} elseif {$hasError == 2 } {
				# If hasError was == 2, it means it's a server issue not a fauly password.. 
				$protocol SendEvent AuthenticationServerError 
			}
			
			$protocol Logout
		}
	}

	method GetContactListTimestamps { } {
		return "0 0"
	}

	method UpdateNickOnServer { username nickname } {
		# TODO FIX THIS
		set cid [::abook::getContactData $username contactguid]
		set command [$commandManager CreateCommand [list $protocol handleSBP] 0 $SBP_COMMAND $cid "MFN" [$protocol urlencode $nickname]]
		$protocol SendCommand $command
		$command destroy
	}

	method UserChangedState {username status {initial 0}} {
		set old_status [[$protocol getDataManager] GetUserStatus $username]
		if {$initial || $old_status != $status} {
			# Send the event to the account manager and let it handle it
			$protocol SendEvent UserChangedState $username $status $initial
			return "STATUS"
		} else {
			return ""
		} 
	}
	method UserChangedNickname {username nickname } {
		if { $nickname != [[$protocol getDataManager] GetUserNickname $username] } {
			# Send the event to the account manager and let it handle it
			$protocol SendEvent UserChangedNickname $username $nickname
			$protocol UpdateNickOnServer $username $nickname
			return "NICKNAME"
		} else {
			return ""
		}

	}
	method UserChangedClientid {username clientid } {
		if { $clientid != [[$protocol getDataManager] GetUserCapabilities $username] } {
			# Send the event to the account manager and let it handle it
			$protocol SendEvent UserChangedCapabilities $username $clientid
			return "CAPABILITIES"
		} else {
			return ""
		}
	}

	method UserChangedMsnObj {username msnobj} {
		if { $msnobj != [[$protocol getDataManager] GetUserDisplayPicture $username] } {
			# Send the event to the account manager and let it handle it
			# TODO change this into something that uses the msnc/msnobj.tcl code... 
			$protocol SendEvent UserChangedDisplayPicture $username $msnobj
			return "DISPLAYPICTURE"
		} else {
			return ""
		}

	}
	method  UserInfoChanged { initial username status nickname clientid msnobj } {
		set infos [list] 
		set info [$protocol UserChangedState $username $status $initial]
		if { $info != "" } {
			lappend infos $info
		}
		set info [$protocol UserChangedNickname $username $nickname]
		if { $info != "" } {
			lappend infos $info
		}
		set info [$protocol UserChangedClientid $username $clientid]
		if { $info != "" } {
			lappend infos $info
		}
		set info [$protocol UserChangedMsnObj $username $msnobj]
		if { $info != "" } {
			lappend infos $info
		}
		
		# TODO : see later how to deal with the initial notification or not..
		if { !$initial && [llength $infos] > 0 } {
			$protocol SendEvent UserInformationUpdated $username $infos
		}
	}

	method SynchronizeContactList { } {
		set command [$commandManager CreateCommand [list $protocol handleSYN] 0 $SYN_COMMAND [$protocol GetContactListTimestamps]]
		$protocol SendCommand $command
		$command destroy
	}

	method PingServer { } {
		# TODO add a way to check if we never received the QNG...
		after cancel $keep_alive_id
		set command [Command create %AUTO% -command $PNG_COMMAND]
		$protocol SendCommand $command
		$command destroy
	}

	method SendInitialPresence { } {
		# We connect as hidden at first in order to handle the ILNs 
		# this is no normal "change state", the callback should handle both the CHG and the ILN commands
		set command [$commandManager CreateCommand [list $protocol handleILN] 1 $CHG_COMMAND $HIDDEN [$protocol GetClientId]]
		$protocol SendCommand $command
		$command destroy

		# Then we will send the event that the CL has been loaded and let the AccountManager send us an event on which real state we should change to..
		$protocol SendEvent ContactListLoaded 

		$protocol ChangePSM [[$protocol getDataManager] GetMyPSM] [[$protocol getDataManager] GetMyMedia]

		# start Pinging the server to avoid disconnected sockets when idled...
		$protocol PingServer


		# TODO transform this into local CCARD info
		::MSNSPACES::InitSpaces

	}

	method ChangeNickname { nick } {
		set command [$commandManager CreateCommand [list $protocol handlePRP] 0 $PRP_COMMAND "MFN" [$protocol urlencode $nick]]
		$protocol SendCommand $command
		$command destroy
	}

	method ChangePSM { psm media} {
		set payload "<Data><PSM>[encoding convertto utf-8 [::sxml::xmlreplace $psm]]</PSM><CurrentMedia>[encoding convertto utf-8 [::sxml::xmlreplace $media]]</CurrentMedia></Data>"	
		set command [$commandManager CreateCommandWithPayload [list $protocol handleUUX $psm $media] 0 $UUX_COMMAND $payload]
		$protocol SendCommand $command
		$command destroy
	}

	method ChangeStatus { status } {
		set command [$commandManager CreateCommand [list $protocol handleCHG] 0 $CHG_COMMAND $status [$protocol GetClientId] [$protocol urlencode [[$protocol getDataManager] GetMyDisplayPicture]]]
		$protocol SendCommand $command
		$command destroy
	}

	method AddUser { username list {groups ""} } {
		# TODO 
	}
	method AcceptUser { username list {groups ""} } {
		# TODO 
	}
	method DeleteUser { username list {groups ""} } {
		# TODO 
	}
	
	method AddGroup { name } {
		set command [$commandManager CreateCommand [list $protocol handleADG] 0 $ADG_COMMAND [$protocol urlencode $name] 0]
		$protocol SendCommand $command
		$command destroy
	}
	
	method DeleteGroup { group } {
		# TODO
	}

	method RenameGroup { group name } {
		# TODO
	}

	method newGroup { groupid groupname } {
		# We send the event tot he account manager
		$protocol SendEvent GroupAdded $groupid $groupname 
	
		#Increment the group count
		incr group_count
		
		# Check if there are no users and we got all LSGs, then we finished the authentification
		if {$group_count == $group_total && $user_total == 0} {
			$protocol SendInitialPresence
		}
	}

	method ListFlagToList { flag } {
		
		set lists [list]
		if { $flag == "" } {
			status_log "${self}:ListFlagToList : List flag is empty. Could not retreive user's lists\n" red
			return $lists
		}
		
		if { $flag & $FORWARD_LIST_FLAG_BIT } {
			lappend lists $FORWARD_LIST
		}
		
		if { $flag & $ALLOW_LIST_FLAG_BIT } {
			lappend lists $ALLOW_LIST
		}
		
		if { $flag & $BLOCK_LIST_FLAG_BIT } {
			lappend lists $BLOCK_LIST
		}
		
		if { $flag & $REVERSE_LIST_FLAG_BIT } {
			lappend lists $REVERSE_LIST
		}
		
		if { $flag & $PENDING_LIST_FLAG_BIT } {
			lappend lists $PENDING_LIST
		}

		return $lists
	}

	method newUser { username nickname contactguid list_names groups } {

		# Send event to the account manager..
		$protocol SendEvent UserAdded $username $nickname $contactguid $list_names $groups

		# Store this user's email for subsequent BPR commands
		set last_lst_user $username

		#Increment the user count
		incr user_count
		
		# Check if there are no users and we got all LSGs, then we finished the authentification
		if {$user_total == $user_count} {
			$protocol SendInitialPresence
		}
	}


	method GetProductKey {} {
		return $PRODUCT_KEY
	}

	method GetProductId {} {
		return $PRODUCT_ID
	}

	method AnswerChallenge { challenge } {
		set algorithm [LockKeyAuthentication create %AUTO%]
		set lockkey [$algorithm CreateLockKey $challenge [$protocol GetProductId] [$protocol GetProductKey]]
		$algorithm destroy

		set command [$commandManager CreateCommandWithPayload [list $protocol handleQRY] 0 $QRY_COMMAND [$protocol GetProductId] $lockkey]
		$protocol SendCommand $command
		$command destroy
	}


	method initCommandManager {cm } {
		set commandManager $cm

		$cm AddAsyncCommand OUT [list $protocol handleOUT]
		$cm AddAsyncCommand BLP [list $protocol handleBLP]
		$cm AddAsyncCommand GTC [list $protocol handleGTC]
		$cm AddAsyncCommand MSG [list $protocol handleMSG]
		$cm AddPayloadCommand MSG
		$cm AddAsyncCommand CHL [list $protocol handleCHL]
		$cm AddAsyncCommand SBS [list $protocol handleSBS]
		$cm AddAsyncCommand FLN [list $protocol handleFLN]
		$cm AddAsyncCommand NLN [list $protocol handleNLN]
		$cm AddAsyncCommand RNG [list $protocol handleRNG]
		$cm AddAsyncCommand LSG [list $protocol handleLSG]
		$cm AddAsyncCommand LST [list $protocol handleLST]
		$cm AddAsyncCommand UBX [list $protocol handleUBX]
		$cm AddPayloadCommand UBX
		$cm AddAsyncCommand ADC [list $protocol handleADC]
		$cm AddAsyncCommand REM [list $protocol handleREM]

		$cm AddAsyncCommand QNG [list $protocol handleQNG]

		$cm AddCommandHandler PRP [list $protocol handlePRP]
		$cm AddCommandHandler BPR [list $protocol handleBPR]

	
		$cm AddPayloadCommand GCF
		
	}

	# Async command handlers
	#

	method handleOUT { command params } {
		# Disconnect if not already done...
		$protocol Logout

		if { [lindex $params 0] == "OTH"} {
			# Send event to the account manager..
			$protocol SendEvent LoggedOut "OTHER"
		} else {
			# Send event to the account manager..
			$protocol SendEvent LoggedOut ""
		}
	}

	method handleBLP { command params } {
		# TODO set user's setting of BLP to AL or BL
		set blp_setting [lindex $params 0]

		# Send event to the account manager..
		$protocol SendEvent NewBuddyListPrivacy $blp_setting
	}
	method handleGTC { command params } {
		# TODO set user's setting of GTC to A or N
		set gtc_setting [lindex $params 0]

		# there was no OLD CODE for this...
	}

	method handleLSG { command params } {
		foreach {groupid groupname} $params break
		set groupname [$protocol urldecode $groupname]
		$protocol newGroup $groupid $groupname
		
	}

	method handleLST { command params } {
		set username ""
		set nickname ""
		set contactguid ""
		set lists ""
		set groups "0"
		
		set state "INFO"
		foreach param $params {
			if {$state == "INFO" } {
				if {[string is digit $param] } {
					set lists $param	
					set state "GROUPS"
				} else {
					foreach {type info} [split $param "="] break
					set type [string toupper $type]
					if {$type == "N" } {
						set username $info
					} elseif {$type == "F" } {
						set nickname [$protocol urldecode $info]
					} elseif {$type == "C" } {
						set contactguid $info
					} else {
						# TODO handle case of unknown info received
					}
				}
			} elseif {$state == "GROUPS" } {
				set groups [split $param ","]
				break
			}
		}
		

		set list_names [$protocol ListFlagToList $lists]
		if {$username != "" } {
			$protocol newUser $username $nickname $contactguid $list_names $groups 
		} else {
			# TODO handle error..
		}
	}
	
	method handleQNG { command params } {
		if { $command == $QNG_COMMAND } {
			# This is the right way to do it, the QNG answer's argument is the number of seconds to wait before the next PNG
			set timer [lindex $params 0]
			set keep_alive_id [after [expr {$timer * 1000}] [list $protocol PingServer]]
		} else {
			# TODO  handle error case
		}
	}
	method handleSBS { command params } {
		# TODO
		# No need to do anything with it...
		# Beleived to be related to your mobile credits...
	}

	method handleCHL { command params } {
		foreach {zero challenge} $params break
		
		if { $zero == 0 } {
			# We received a challenge, answer it
			$protocol AnswerChallenge $challenge
		} else {
			# TODO handle it some way...
			status_log "Invalid challenge\n" red
		}
	}

	method handleFLN { command params } {
		set username [lindex $params 0]
		set info [$protocol UserChangedState $username $OFFLINE]
		if { $info != "" } {
			$protocol SendEvent UserInformationUpdated $username $info
		}
		
	}
	method handleNLN { command params } {
		foreach {status username nickname clientid msnobj} $params break
		set nickname [$protocol urldecode $nickname]
		set msnobj [$protocol urldecode $msnobj]
		$protocol UserInfoChanged 0 $username $status $nickname $clientid $msnobj
	}

	method handleUBX { command params payload } {
		set username [lindex $params 0]
		if {$payload != ""} {
			if { [catch { set xml [xml2list $payload] } ] } {
				return
			}
			set psm [encoding convertfrom utf-8 [GetXmlEntry $xml "Data:PSM"]]
			set currentMedia  [encoding convertfrom utf-8 [GetXmlEntry $xml "Data:CurrentMedia"]]
		} else {
			set psm ""
			set currentMedia ""
		}
		if { $psm != [[$protocol getDataManager] GetUserPSM $username]  || 
		     $currentMedia != [[$protocol getDataManager] GetUserMedia $username] } {
			# send the new information to the account manager to handle it
			$protocol SendEvent UserPSMChanged $username $psm $currentMedia
		}
		
	}

	method handleMSG { command params payload } {
		# TODO see cmsn_ns_msg (protocol.tcl) and hotmail_procmsg (hotmail.tcl)
	}

	method handleRNG { command params } {
		# TODO
	}


	# trid/async command handlers
	#
	method handlePRP { command params } {
		if { $command == $PRP_COMMAND } {
			foreach {key value_encoded} $params break
			
			set value [$protocol urldecode $value_encoded]
			
			# Send event to the account manager..
			$protocol SendEvent NewPersonalInformation $key $value

			if {$key == "MFN" } {
				# Send specific event for the nickname
				$protocol SendEvent MyNicknameChanged $value				
			}
		} elseif {$command == 209 } {
			$protocol SendEvent InvalidUsername
		}
	} 
	
	

	method handleBPR { command params } {
		foreach {key value_encoded} $params break

		set value [$protocol urldecode $value_encoded]

		if {$last_lst_user != "" } {
			# Send event to the account manager..
			$protocol SendEvent NewUserInformation $last_lst_user $key $value
		}
	}

	method handleSBP { command params } {
		# TODO do we need to do something here ? old code totally ignored it :s
	}

	# trid command handlers
	#
	method handleUSR {command params } {
		if {$command == $USR_COMMAND} {
			set response [lindex $params 0]
			if {$response == [$protocol GetAuthenticationMethod] } {
				foreach {algorithm status url} $params break
				if { $status == "S" } {
					# Create an authenticator depending on this protocol's algorithm
					if { ![catch {set auth [${algorithm}Authentication create %AUTO%]}] } {
						if {$authenticator != "" } {
							$authenticator destroy
							set authenticator ""
						}

						# Send event to the account manager..
						$protocol SendEvent Authenticating $algorithm

						set authenticator $auth
						$auth Authenticate [list $protocol AuthenticationCompleted] $url
					} else {
						# TODO unsupported auth method...
					}
				}
			} elseif {$response == "OK" } {
				# We finished authenticating, now we need to synchronize the contact list (SYN command)
				foreach {ok email verified zero} $params break
				$protocol SynchronizeContactList

				# Send event to the account manager..
				$protocol SendEvent Authenticated 

				status_log "connected with $email which is a verified ($verified) address"
			}
		} elseif {$command == $XFR_COMMAND } {
			$protocol handleXFR $command $params
		} else {
			# Send event to the account manager..
			$protocol SendEvent AuthenticationFailed 

			$protocol Logout
		}

	}
	method handleXFR { command params } {
		foreach {type address method auth} $params break
		# TODO complete this...
		if {$type == "NS" } {
			# TODO review this... should the accountmanager reconnect us or should we do it on our own ?
			$protocol SendEvent ConnectionRedirected $address
		} elseif {$type == "SB" } {
		} else {
			# TODO unsupported server type	 
		}
	}

	method handleCHG { command params } {
		foreach {status clientid msnobj} $params break
		set msnobj [$protocol urldecode $msnobj]
		# Send event to the account manager..
		$protocol SendEvent MyStatusChanged $status $clientid $msnobj
	}

	method handleILN { command params } {
		# TODO review this
		if {$command == "ILN" } {
			foreach {status username nickname clientid msnobj} $params break
			set msnobj [$protocol urldecode $msnobj]
			set nickname [$protocol urldecode $nickname]
			$protocol UserInfoChanged 1 $username $status $nickname $clientid $msnobj
		} elseif {$command == "CHG" } {
			$protocol handleCHG $command $params
		}
	}


	# This command is special because when PSM was changed successfully, we only receive a UUX trID 0
	# So I need to pass the new psm and media to the handler as separate args myself.
	method handleUUX { psm media command params } {
		if { [lindex $params 0] == 0 } {
			if { $psm != [[$protocol getDataManager] GetMyPSM] ||
			     $media != [[$protocol getDataManager] GetMyMedia] } {
				# send the new information to the account manager to handle it
				$protocol SendEvent MyPSMChanged $username $psm $media
			}
		} else {
			# TODO handle possible error here...
		}
	}

	method handleADC { command params } {
		# TODO 
	}

	method handleADG { command params } {
		if {$command == $ADG_COMMAND} {
			foreach {groupid groupname} $params break
			set groupname [$protocol urldecode $groupname]
			$protocol newGroup $groupid $groupname
		} else {
			# TODO handle errors for ADG
		}
		
	}

	method handleREM { command params } {
		# TODO 
	}

	method handleQRY { command params } {
		if {$command == $QRY_COMMAND } {
			# Everything's good, our challenge was accepted...
		} else {
			# TODO handle challenge errors...
		}
	}

	method handleGCF { command params payload } {
		# TODO 
		# Nothing to do here either, who cares about that Shields.xml config file ? it only restricts the client with the banned word or something... ?
	}
	method handleSYN { command params } {
		if {$command == $SYN_COMMAND } {
			foreach {timestamp1 timestamp2 user_total group_total } $params break

			# Send event to the account manager..
			$protocol SendEvent LoggedIn 

			# Check if there are no users and no groups, then we already finished authentification
			if { $group_total == 0 && $user_total == 0} {
				$protocol SendInitialPresence
			}
		} else {
			# TODO handle error
		}
	}
}

