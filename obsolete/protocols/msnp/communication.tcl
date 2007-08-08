

# TODO : Wrap this up with a Connection object AND Proxy object, THIS IS BASIC FOR NOW, ONLY FOR TESTING!
# this should be easy to read/use, the proxy object takes cares itself of looking at ::config, no need to configure -proxy or anything... 
snit::type MSNPSocket {
	option -handler ""
	option -server ""
	variable socket ""
	variable inBuffer ""
	
	destructor {
		$self Close
	}
	method Close {} {
		if { $socket != "" } {
			close $socket
			set socket ""
		}
	}
	method isConnected { } {
		return [expr {$socket != "" && ![eof $socket] && [fconfigure $socket -error] == ""} ]
	}

	method connect { } {
		set server $options(-server)
		status_log "${self}::connect connecting to $server" 
		if {$server != "" } {
			foreach {host port} [split $server ":"] break
			if { $port == "" } { set port 1863 }
			if { [catch {set socket [socket -async $host $port] } ] } {
				
			} else {
				fconfigure $socket -blocking 0 -translation {binary binary} -buffering none
				fileevent $socket readable [list $self handleConnected]
				fileevent $socket writable [list $self handleConnected]
			}
		}
	}
	method handleData { } {
		append inBuffer [read $socket]
		append inBuffer [read $socket]
		if { [$self lineAvailable] }  {
			if {$options(-handler) != "" } {
				eval $options(-handler) $self "DATA"
			}
			
			# check if we didn't get destroyed  during the last data handling
			# check if we have any more input that we received and didn't consume yet.
			if { [info command $self] == $self && [$self lineAvailable] } { 
				$self handleData	
			}
		} elseif { [eof $socket] } {
			$self Close
			if {$options(-handler) != "" } {
				eval $options(-handler) $self "DISCONNECTED"
			}
		} 
		
	}
	method lineAvailable { } {
		return [expr {[string first "\r\n" $inBuffer] != -1}]
	}
	method handleConnected { } {
		fileevent $socket writable [list]
		fileevent $socket readable [list $self handleData]
		
		if { [eof $socket] || [fconfigure $socket -error] != ""} {
			$self Close
			if {$options(-handler) != "" } {
				eval $options(-handler) $self "ERROR"
				
			}
		} else {
			if {$options(-handler) != "" } {
				eval $options(-handler) $self "CONNECTED"
			}
		}
	}

	method SendLN { data } {
		status_log "${self}:SendLN : >> $data\r\n" green
		puts -nonewline $socket "${data}\r\n"
	}
	method Send { data } {
		status_log "${self}:Send : >> $data" green
		puts -nonewline $socket $data
	}
	method GetLine {} {
		set idx [string first "\r\n" $inBuffer]
		if {$idx != -1 } {
			set data [string range $inBuffer 0 [expr {$idx -1}]]
			set inBuffer [string range $inBuffer [expr {$idx + 2}] end]
		} else {
			set data ""
		}
		status_log "${self}:GetLine : << $data" red
		return $data
	}
	method Get {size} {
		while {[string length $inBuffer] < $size } {
			update
			after 100
		}

		set data [string range $inBuffer 0 [expr {$size -1}]]
		set inBuffer [string range $inBuffer $size end]
		status_log "${self}:Get : << $data" red
		return $data
	}
}