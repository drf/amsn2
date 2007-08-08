# TODO move to directory called 'core'

namespace eval ::Events {

	variable eventsArray

	# sends to all interested listeners the event that occured
	# eventName: name of the event that happened
	# layer : The layer from which the event was sent, can be protocol/data/gui 
	# caller:    the object that fires the event, set to all to
	#            notify all listeners for all events with that name
	proc fireEvent { eventName layer caller args } {
		variable eventsArray
		status_log "Received event : $eventName from $layer : $caller with args : $args"
		#fire events registered for both the current caller and 'all'
		foreach lay [list $layer "all"] {
			foreach call [list $caller "all"] {
				#first check there were some events registered to caller or it will fail
				if { [info exists eventsArray($eventName,$lay,$call)] } {
					foreach listener [set eventsArray($eventName,$lay,$call)] {
						status_log "Calling registered event $listener"
						eval $listener [linsert $args 0 $eventName $layer $caller]
					}
				}
			}
		}
	}

	# registers a listener for an event
	# the listener has to have a method the same as the eventName
	# eventName: name of the event to listen to
	# layer : The layer from which the event is sent, can be protocol/data/gui 
	# caller:    the object that fires the event, set to all to
	#            register for all events with that name
	# listener:  the object that wants to receive the events
	proc registerEvent { eventName layer caller listener } {
		variable eventsArray
		lappend eventsArray($eventName,$layer,$caller) $listener
	}
	
	proc unregisterEvent { eventName layer caller listener } {
		variable eventsArray
		if { [info exists eventsArray($eventName,$layer,$caller)] } {
			set idx [lsearch [set eventsArray($eventName,$layer,$caller)] $listener]
			if { $idx != -1 } {
				set eventsArray($eventName,$layer,$caller) [lreplace $eventsArray($eventName,$layer,$caller) $idx $idx]
			} else {
				status_log "ERROR: tried to unregister an unexistant event: $eventName,$caller" white
			}
		}
	}

}