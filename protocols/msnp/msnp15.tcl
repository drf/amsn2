

snit::type MSNP15 {
	delegate method * to parent_proto
	delegate option * to parent_proto
	option -protocol -default "" -configuremethod ProtocolOptionChanged
	variable protocol
	variable commandManager
	
	constructor {args} {
		set options(-protocol) [set protocol $self]
		set parent_proto [eval MSNP14 create %AUTO% $args]
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
	method handleUSR { } {
	}
	
}