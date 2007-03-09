
snit::type MSNP12 {
	delegate option * to parent_proto
	delegate method * to parent_proto
	option -protocol -default "" -configuremethod ProtocolOptionChanged
	variable protocol
	variable commandManager 

	# TODO set the client version to a real client that uses MSNP12
	variable CLIENT_VERSION "8.0.0812"
	variable PRODUCT_KEY "YMM8C_H7KCQ2S_KL"
	variable PRODUCT_ID "PROD0090YUAUV\{2B"

	variable LST_COMMAND "LST"
	variable LKP_COMMAND "LKP"
	variable NOT_COMMAND "NOT"
	

	constructor {args} {
		set options(-protocol) [set protocol $self]
		set parent_proto [eval MSNP11 create %AUTO% $args]
		$self configurelist $args
		$parent_proto configure -protocol $options(-protocol)
	}

	destructor {
		$parent_proto destroy
	}

	method ProtocolOptionChanged {option value} {
		set options($option) $value
		if {$options(-protocol) == "" } {
			set options(-protocol) $self
		}
		set protocol $options(-protocol)
	}
	method initCommandManager {cm } {
		set commandManager $cm
		$parent_proto initCommandManager $cm

		$cm AddAsyncCommand NOT [list $protocol handleNOT]
		$cm AddAsyncCommand LST [list $protocol handleLST]
	}

	method GetClientVersion { } {
		return $CLIENT_VERSION
	}

	method GetProductKey {} {
		return $PRODUCT_KEY
	}

	method GetProductId {} {
		return $PRODUCT_ID
	}


	# Async command handlers
	#

	method handleNOT { command params } {
		# TODO 
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
					set state "UNKNOWN_FIELD"
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
			} elseif {$state == "UNKNOWN_FIELD" } {
				# TODO we ignore this unknown field for now..
				set state "GROUPS"
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
	
}

