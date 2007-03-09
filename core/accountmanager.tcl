package require aMSN2_Protocols

# TODO  this should all change into a static class -> typevariable/typemethods, so we can drop the singleton.

snit::type AccountManager {
	# TODO, these should definitely change to something non-protocol related... 
	typevariable ONLINE "NLN"
	typevariable AWAY "AWY"
	typevariable IDLE "IDL"
	typevariable BUSY "BSY"
	typevariable OFFLINE "FLN"
	typevariable HIDDEN "HDN"
	typevariable BRB "BRB"
	typevariable PHONE "PHN"
	typevariable LUNCH "LUN"

	typevariable FORWARD_LIST "FL"
	typevariable ALLOW_LIST "AL"
	typevariable BLOCK_LIST "BL"
	typevariable REVERSE_LIST "RL"
	typevariable PENDING_LIST "PL"

	typevariable msnp ""

	typemethod InitEvents { } {
		::Events::registerEvent Connected protocol all [list AccountManager Connected] ;# On socket connected
		::Events::registerEvent DisConnected protocol all [list AccountManager DisConnected] ;# On socket disconnected
		::Events::registerEvent ConnectionRedirected protocol all [list AccountManager ConnectionRedirected] ; # On XFR
		::Events::registerEvent LoggedIn protocol all [list AccountManager LoggedIn] ;# On the SYN command
		::Events::registerEvent LoggedOut protocol all [list AccountManager LoggedOut] ; # On an OUT command
		::Events::registerEvent Authenticating protocol all [list AccountManager Authenticating] ;# when USR TWN/SSO is received
		::Events::registerEvent Authenticated protocol all [list AccountManager Authenticated] ;# when USR OK is received
		::Events::registerEvent AuthenticationFailed protocol all [list AccountManager AuthenticationFailed] ;# when wrong user/pass
		::Events::registerEvent AuthenticationServerError protocol all [list AccountManager AuthenticationServerError] ;# when auth server inaccessible...
		::Events::registerEvent GroupAdded protocol all [list AccountManager GroupAdded] ; # Sent on LSG or ADG
		::Events::registerEvent UserAdded protocol all [list AccountManager UserAdded] ; # on LST
		::Events::registerEvent ContactListLoaded protocol all [list AccountManager ContactListLoaded] ; # when we finished loading all LSG and LST
		::Events::registerEvent MyStatusChanged protocol all [list AccountManager MyStatusChanged] ; # On CHG
		::Events::registerEvent NewBuddyListPrivacy protocol all [list AccountManager NewBuddyListPrivacy] ; # On BLP
		::Events::registerEvent UserChangedState protocol all [list AccountManager UserChangedState] ; # on ILN/NLN
		::Events::registerEvent UserChangedNickname protocol all [list AccountManager UserChangedNickname] ; # on ILN/NLN
		::Events::registerEvent UserChangedCapabilities protocol all [list AccountManager UserChangedCapabilities] ; # on ILN/NLN
		::Events::registerEvent UserChangedDisplayPicture protocol all [list AccountManager UserChangedDisplayPicture] ; # on ILN/NLN
		::Events::registerEvent UserPSMChanged protocol all [list AccountManager UserPSMChanged] ; # On UBX
		::Events::registerEvent MyPSMChanged protocol all [list AccountManager MyPSMChanged] ; # On UUX
		::Events::registerEvent MyMediaChanged protocol all [list AccountManager MyMediaChanged] ; # On UUX
		::Events::registerEvent MyStatusChanged protocol all [list AccountManager MyStatusChanged] ; # On CHG
		::Events::registerEvent NewPersonalInformation protocol all [list AccountManager NewPersonalInformation] ; # On PRP
		::Events::registerEvent MyNicknameChanged protocol all [list AccountManager MyNicknameChanged] ; # On PRP
		::Events::registerEvent InvalidNicknameChange protocol all [list AccountManager InvalidNicknameChange] ; # On 209 error response to PRP
		::Events::registerEvent NewUserInformation protocol all [list AccountManager NewUserInformation] ; # On BPR
	}


	typemethod Connect { } {
		if { $msnp != "" } {
			$msnp destroy
			set msnp ""
		}
		set msnp [MSNP create %AUTO% -server [::config::getKey start_ns_server] -login [::config::getKey login]]
		# TODO, we should send an event to the protocol, asking it to connect itself
		$msnp Connect

		return $msnp
	}
	typemethod DisConnect { } {
		if { $msnp != "" } {
			# TODO, we should send an event to the protocol, asking it to disconnect itself
			$msnp Logout
			$msnp destroy
			set msnp ""
		}

		return $msnp
	}

	typemethod Connected { event layer caller} {
		cmsn_draw_signin
		::Event::fireEvent loggingIn protocol
	}

	typemethod DisConnected { event layer caller} {
		::Event::fireEvent loggedOut protocol
	}

	typemethod ConnectionRedirected {event layer caller address} {
		::config::setKey start_ns_server $address
		$caller configure -server $address
		$caller Connect
	}

	typemethod LoggedIn { event layer caller} {
		set dm [$caller getDataManager]
		if {$dm != "" } {
			$dm destroy
		}
		$caller setDataManager [DataManager create %AUTO% -login [$caller cget -login]]
	}

	typemethod LoggedOut { event layer caller reason } {
		# TODO this should be duplicated in disconnected, no ?

		set dm [$caller getDataManager]
		if {$dm != "" } {
			set mystatus [$dm GetMyStatus]
			$dm destroy
		} else {
			set mystatus $OFFLINE
		}


		if {$reason == "OTHER" }  {
			msg_box "[trans loggedotherlocation]"
			status_log "Logged other location\n" red
			$caller destroy
		} else {
			# TODO review this here...
			::config::setKey start_ns_server [::config::getKey default_ns_server]
			if { [::config::getKey reconnect] == 1 } {
				set ::oldstatus $mystatus

				# TODO make it use an event to the GUI manager
				cmsn_draw_reconnect "[trans servergoingdown]"
				after 5000 [list $caller Connect]
			} else {
				msg_box "[trans servergoingdown]"
				$caller destroy
			}
		}
	}
	
	typemethod Authenticating { event layer caller algorithm } {
		# TODO we should update GUI 'logging in' window to show progress
	}

	typemethod Authenticated { event layer caller  } {
		# TODO we should update GUI 'logging in' window to show progress
	}

	typemethod AuthenticationFailed { event layer caller  } {
		status_log "Error: User/Password\n" red
		::amsn::errorMsg "[trans baduserpass]"
	}

	typemethod AuthenticationServerError { event layer caller  } {
		::amsn::errorMsg "[trans connecterror]"
	}

	typemethod ChCustomState { caller dm idx } {
		global HOME automessage automsgsent original_nick original_psm
		set automessage "-1"
		set redraw 0
		if { [string is digit $idx] == 1 } {
			if { [lindex [StateList get $idx] 2] != "" } {
				if {![info exists original_nick]} {
					set original_nick [$dm GetMyNickname]
				}
				if {![info exists original_psm]} {
					set original_psm [$dm GetMyPSM]
				}
				#set new_state [lindex [lindex $list_states [lindex [StateList get $idx] 2]] 0]
				set new_state [::MSN::numberToState [lindex [StateList get $idx] 2]]
				if { $new_state == [$dm GetMyStatus] } {
					set redraw 1
				}
				set automessage [StateList get $idx]
				set newname "[lindex [StateList get $idx] 1]"
				set newpsm "[lindex [StateList get $idx] 5]"
				status_log [StateList get $idx]
				if { $newname != "" } {
					catch {
						set nickcache [open [file join ${HOME} "nick.cache"] w]
						fconfigure $nickcache -encoding utf-8
						puts $nickcache $original_nick
						puts $nickcache $newname
						puts $nickcache [$caller cget -login]
						close $nickcache
					}
					
					set newname [string map { "\\" "\\\\" "\$" "\\\$" } $newname]
					set newname [string map { "\\\$nick" "\${original_nick}" } $newname]
					set newname [subst -nocommands $newname]
					$caller ChangeNickname $newname
					StateList promote $idx
				}
				if { $newpsm != "" } {
					catch {
						set psmcache [open [file join ${HOME} "psm.cache"] w]
						fconfigure $psmcache -encoding utf-8
						puts $psmcache $original_psm
						puts $psmcache $newpsm
						puts $psmcache  [$caller cget -login]
						close $psmcache
					}
					
					set newpsm [string map { "\\" "\\\\" "\$" "\\\$" } $newpsm]
					set newpsm [string map { "\\\$psm" "\${original_psm}" } $newpsm]
					set newpsm [subst -nocommands $newpsm]
					$caller ChangePSM $newpsm
				}
			}
		} else {
			set automessage "-1"
			if { $idx == [$dm GetMyStatus]} {
				set redraw 1
			}
			if {[::config::getKey storename]} {
				if { [info exists original_nick] } {
					$caller ChangeNickname $original_nick
					unset original_nick
					catch { file delete [file join ${HOME} "nick.cache"] }
				}
				if { [info exists original_psm] } {
					$caller ChangePSM $original_psm
					unset original_psm
					catch { file delete [file join ${HOME} "psm.cache"] } 
				}
			}
			set new_state $idx
		}
		
		if { [info exists new_state] } {
			$caller ChangeStatus $new_state
			
			#PostEvent 'ChangeMyState' when the user changes his/her state
			set evPar(automessage) automessage
			set evPar(idx) new_state
			::plugins::PostEvent ChangeMyState evPar
		} else {
			status_log "ChCustomState where state didnt exist !!!" red
		}
		
		
		CreateStatesMenu .my_menu
		if { [info exists automsgsent] } {
			unset automsgsent
		}
		if { $redraw == 1 } {
			cmsn_draw_online 0 1
		}
	}
	
	typemethod ContactListLoaded { event layer caller  } {
		set dm [$caller getDataManager]
		#Don't use oldstatus if it was "FLN" (disconnectd) or we will get a 201 error
		if {[info exists ::oldstatus] && $::oldstatus != "FLN" } {
			AccountManager ChCustomState $caller $dm $::oldstatus
			send_dock "STATUS" $::oldstatus
			unset ::oldstatus
		} elseif {![is_connectas_custom_state [::config::getKey connectas]]} {
			#Protocol code to choose our state on connect
			set number [get_state_list_idx [::config::getKey connectas]]
			set goodstatecode "[::MSN::numberToState $number]"

			if {$goodstatecode != ""} {
				AccountManager ChCustomState $caller $dm "$goodstatecode"
				send_dock "STATUS" "$goodstatecode"
			} else {
				status_log "Not able to get choosen key: [::config::getKey connectas]"
				AccountManager ChCustomState $caller $dm "NLN"
				send_dock "STATUS" "NLN"
			}
		} else {
			set idx [get_custom_state_idx [::config::getKey connectas]]
			AccountManager ChCustomState $caller $dm $idx
			if { [lindex [StateList get $idx] 2] != "" } {
				set new_state [::MSN::numberToState [lindex [StateList get $idx] 2]]
				send_dock "STATUS" "$new_state"
			}
		}



		$dm Save
		set ::contactlist_loaded 1

		after 0 { 
			cmsn_draw_online 1

			#Update Preferences window if it's open
			after 1000 {catch {InitPref 1}}
		}

		::Event::fireEvent contactlistLoaded protocol
		::plugins::PostEvent contactlistLoaded evPar

		cmsn_draw_online 1 2
	}

	typemethod NewBuddyListPrivacy {event layer caller privacy } {
		[$caller getDataManager] SetBuddyListPrivacy $privacy
	}

	typemethod NewPersonalInformation { event layer caller key value} {
		[$caller getDataManager] SetPersonalInformation $key $value
	}

	typemethod NewUserInformation { event layer caller username key value} {
		[$caller getDataManager] SetUserInformation $username $key $value
	}

	typemethod UserAdded { event layer caller username nickname contactguid list_names groups } {
		[$caller getDataManager] AddUser $username $nickname $contactguid $list_names $groups
	}

	typemethod GroupAdded { event layer caller groupid groupname } {
		[$caller getDataManager] AddGroup  $groupid $groupname
	
	}

	typemethod UserPSMChanged { event layer caller username psm media } {
		[$caller getDataManager] SetUserPSM $username $psm $media
	}

	typemethod UserChangedState { event layer caller username status initial} {
		[$caller getDataManager] SetUserStatus $username $status

		::Event::fireEvent contactStateChange protocol $username
		::plugins::PostEvent ChangeState evpar
	}

	typemethod UserChangedNickname { event layer caller username nickname } {
		::abook::setContactData $username nick $nickname
		::Event::fireEvent contactNickChange protocol $username
	}

	typemethod UserChangedCapabilities { event layer caller username capabilities } {

	}

	typemethod UserChangedDisplayPicture { event layer caller username msnobj } {

	}


	typemethod MyNicknameChanged { event layer caller nick} {
		# We don't need to save the new nickname because it gets saved on the event NewPersonalInformation
		

		# TODO why would we update the tray dock on nick change? :|
		send_dock STATUS [[$caller getDataManager] GetMyStatus]
		#an event used by guicontactlist to know when we changed our nick
		::Event::fireEvent myNickChange protocol
	}

	typemethod InvalidNicknameChange { event layer caller} {
		msg_box [trans invalidusername]
	}

	typemethod MyPSMChanged { event layer caller psm media} {
		[$caller getDataManager] SetMyPSM $psm $media
		save_config
	}

	typemethod MyStatusChanged { event layer caller status clientid msnobj } {
		[$caller getDataManager] SetMyStatus $status
		[$caller getDataManager] SetMyDisplayPicture $msnobj

		cmsn_draw_online 1 1

		#Alert dock of status change
		send_dock "STATUS" $status
	}

}


AccountManager InitEvents