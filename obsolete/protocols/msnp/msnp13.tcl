
snit::type MSNP13 {
	delegate option * to parent_proto
	delegate method * to parent_proto
	option -protocol -default "" -configuremethod ProtocolOptionChanged
	variable protocol
	variable commandManager
	
	constructor {args} {
		set options(-protocol) [set protocol $self]
		set parent_proto [eval MSNP12 create %AUTO% $args]
		$self configurelist $args
		$parent_proto configure -protocol $options(-protocol)

		error "PROTOCOL VERSION NOT YET SUPPORTED"
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
	method handleADL { } {
	}
	
	method initCommandManager {cm } {
		set commandManager $cm
		$parent_proto initCommandManager $cm

		$cm AddPayloadCommand ADL
		$cm AddPayloadCommand RML
		$cm AddPayloadCommand UBN
	}
}

