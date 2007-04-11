
::snit::type MSNP {
	option -protocols [list MSNP12 MSNP11] ;# Add MSNP15 here once the SSOAuthentication method is written
	delegate method * to api
	option -server
	option -login
	variable socket ""
	variable status ""
	variable protocol ""
	variable protocol_version ""
	variable commandManager
	variable dataManager ""

	variable VER_COMMAND "VER"
	variable CVR_COMMAND "CVR"
	variable OUT_COMMAND "OUT"

	variable CVR_PROTOCOL "CVR0"

	# CVR information
	variable LOCALE_ID "0x0409"
	variable OS_TYPE "winnt"
	variable OS_VERSION "5.1"
	variable ARCHITECTURE "i386"
	variable CLIENT_NAME "MSNMSGR"
	variable MSMSGS "msmsgs"

	constructor {args} {
		$self configurelist $args

		package require http
		package require tls

		http::register https 443 ::tls::socket

		set commandManager [CommandManager create %AUTO%]
		set api [ProtocolAPI create %AUTO%]
	}

	destructor {
		$self Logout
	}

	method test { } {
		puts [myvar protocol]
	}

	method getDataManager { } {
		return $dataManager
	}
	method setDataManager { manager } {
		set dataManager $manager
	}

	method SendEvent { event args} {
		# Send protocol event to the account manager..
		eval [linsert $args 0 ::Events::fireEvent $event protocol $self]
	}

	method Connect { } {
		$self Logout

		set socket [MSNPSocket create %AUTO%]
		$socket configure -handler [list $self handleSocketEvent]
		$socket configure -server $options(-server)
		$socket connect
	}

	method Logout { } {
		if {$protocol != "" } {
			$protocol destroy
			set protocol ""
		}

		if { $socket != ""  && [$socket isConnected] } {
			set command [Command create %AUTO% -command $OUT_COMMAND]
			$self SendCommand $command
			$command destroy
		}
		$self CloseSocket
	}

	method CloseSocket { } {
		if { $socket != "" } {
			$socket destroy
			set socket ""
			$self SendEvent DisConnected
		}
		set status "DISCONNECTED"
	}


	method SendCommand { command } {
		$socket Send [$command toString]
	}

	method handleSocketEvent {sock event} {
		if { $sock != $socket } {
			status_log "${self}::handleSocketEvent sock != socket | $sock != $socket" red
			return
		}
		switch -- $event {
			"CONNECTED" {
				#status_log "${self}::handleSocketEvent Connected" red
				$self SendEvent Connected

				set com [$commandManager CreateCommand [list $self handleVER] 0 $VER_COMMAND $options(-protocols) $CVR_PROTOCOL]
				$self SendCommand $com
				$com destroy
				set status "CONNECTED"
			}
			"DATA" {
				set data [$socket GetLine]
				status_log "${self}::handleSocketEvent Received $data" red
				set payload_size [$commandManager GetPayloadSize $data]
				if { $payload_size > 0 } {
					set payload [$socket Get $payload_size]
				}  else {
					set payload ""
				}
				$commandManager HandleCommand $data $payload
			}
			"DISCONNECTED" {
				status_log "${self}::handleSocketEvent received disconnection" red
				$self CloseSocket
			}
			"ERROR" {
				status_log "${self}::handleSocketEvent error connecting to server" red
				$self CloseSocket
				$self SendEvent ErrorConnecting
			}
			
			
		}
	}

	method handleVER { command params} {
		if {$command == $VER_COMMAND } {
			set proto [lindex $params 0]
			
			if { $proto != $CVR_PROTOCOL } {
				if { ![catch { set protocol_obj [$proto create %AUTO% -msnp $self]} res ] } {
					set protocol_version $proto
					if { $protocol != ""} {
						$protocol destroy
					}
					set protocol $protocol_obj
					$api configure -protocol $protocol

					$protocol initCommandManager $commandManager

					set com [$commandManager CreateCommand [list $self handleCVR] 0 $CVR_COMMAND $LOCALE_ID $OS_TYPE $OS_VERSION $ARCHITECTURE $CLIENT_NAME [$protocol GetClientVersion] $MSMSGS $options(-login)]
					$self SendCommand $com
					$com destroy

				} else {
					status_log "${self}::handleVER unable to instanciate protocol version $proto : $command $params -- $res -- $::errorInfo" red
					
				}
			} else {
				status_log "${self}::handleVER no protocol supported by server : $command $params" red
				# TODO : normally, we should send a CVQ message to know if we have the 'latest' version of MSN, but we don't care, right? :p
			}
		} else {
			status_log "${self}::handleVER received non standard message : $command $params" red
			$self Logout
		}
	}

	method handleCVR { command params } {
		if {$command == $CVR_COMMAND } {
			# we ignore this information, we only need to authenticate and send the USR command now...
			$protocol Authenticate
		} else {
			# TODO handle error
		}
	}
	
}

snit::type Command {
	option -command ""
	option -trid ""
	option -params ""
	option -payload ""
	option -haspayload 0

	method generateCommand  { } {
	}

	method toString { } {
		set command $options(-command)
		if { $options(-trid) != "" } {
			set command [join [list $command $options(-trid)] " "]
		}
		if { $options(-params) != "" } {
			set command [join [list $command [join $options(-params)]] " "]
		}
		if {$options(-haspayload)} {
			set length [string length $options(-payload)]
			set command [join [list $command $length] " "]
			append command "\r\n"
			append command $options(-payload)
		} else {
			append command "\r\n"
		}
		return $command
	}
}

snit::type CommandManager {
	variable payload_commands [list]
	variable async_commands [list]
	variable transactionId 0
	variable tridHandlers
	variable persistent_trids [list]
	variable commandHandlers

	constructor {args} {
		# seems not to work.. maybe because I have no 'options'
		# $self configurelist $args

		array set tridHandlers [list]
		array set commandHandlers [list]
	}

	method NextTrID { handler } {
		set trid [incr transactionId]
		set tridHandlers($trid) $handler
		return $trid
	}

	method GetPayloadSize { data } {
		set elements [split $data " "]
		set command [lindex $elements 0]
		set length [lindex $elements end]
		if { [lsearch -exact $payload_commands $command] != -1 } {
			return $length
		} else {
			return 0
		}
	}
	method HandleCommand { data {payload ""} } {
		set elements [split $data " "]
		set command [lindex $elements 0]

		if { [string length $command] > 0 } {
			
			if { [lsearch -exact $async_commands $command] == -1 } {
				set trid [lindex $elements 1]
				set params [lrange $elements 2 end]
				
				if {[info exists tridHandlers($trid)] } {
					set handler [set tridHandlers($trid)]
					
					# if the command is not persistent, then we can free the memory used by its trid handler
					if { [lsearch -exact $persistent_trids $trid] == -1 } {
						array unset tridHandlers $trid
					}

					if { [lsearch -exact $payload_commands $command] != -1 } {
						# We remove the payload size from the params...
						set params [lrange $params 0 end-1]
						return [eval $handler $command [list $params] [list $payload]]
					} else {
						return [eval $handler $command [list $params]]
					}
				} 
			}
			if {[info exists commandHandlers($command)] } {
				set params [lrange $elements 1 end]
				
				set handler [set commandHandlers($command)]
				if { [lsearch -exact $payload_commands $command] != -1 } {
					# We remove the payload size from the params...	
					set params [lrange $params 0 end-1]
					return [eval $handler $command [list $params] [list $payload]]
				} else {
					return [eval $handler $command [list $params]]
				}
			} else {
				status_log "${self}::HandleCommand non async command has no trid/command Handler : $data" red	
			}
		}
	}

	method AddPayloadCommand { command } {
		lappend payload_commands $command
	}

	method AddAsyncCommand { command handler} {
		lappend async_commands $command
		$self AddCommandHandler $command $handler
	}

	method AddCommandHandler { command handler } {
		set commandHandlers($command) $handler
	}

	method CreateCommand {handler persistent command args} {
		set com [Command create %AUTO% -command $command -trid [$self NextTrID $handler] -params $args -haspayload 0]
		if {$persistent} {
			lappend persistent_trids [$com cget -trid]
		}
		return $com
	}

	method CreateCommandWithPayload {handler persistent command args} {
		set parameters [lrange $args 0 end-1]
		set payload [lindex $args end]
		set com [Command create %AUTO% -command $command -trid [$self NextTrID $handler] -params $parameters -payload $payload -haspayload 1]
		if {$persistent} {
			lappend persistent_trids [$com cget -trid]
		}
		return $com
	}
}
