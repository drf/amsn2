snit::type DataManager {
	option -login

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


	constructor { args } {
		$self configurelist $args
		
		# TODO OLD CODE
		::MSN::clearList FL
		::MSN::clearList BL
		::MSN::clearList RL
		::MSN::clearList AL
		::groups::Reset
		::groups::Set 0 [trans nogroup]
	}

	destructor {
		::abook::lastSeen

		::log::eventlogout

		global automessage

		::MSN::setMyStatus FLN

		::groups::Disable

		::abook::saveToDisk

		global list_BLP emailBList
		::MSN::clearList AL
		::MSN::clearList BL
		::MSN::clearList FL
		::MSN::clearList RL

		set list_BLP -1
		if { [info exists emailBList] } {
			unset emailBList
		}

		::abook::unsetConsistent

		#Try to update Preferences
		catch {InitPref 1}

		set automessage "-1"


		#an event to let the GUI know we are actually logged out now
		::Event::fireEvent loggedOut protocol

		cmsn_draw_offline

		#Set all CW users as offline
		foreach user_name [::abook::getAllContacts] {
			::abook::setVolatileData $user_name state "FLN"
		}

		foreach chat_id [::ChatWindow::getAllChatIds] {
			::ChatWindow::TopUpdate $chat_id
		}

		#Alert dock of status change
		#      send_dock "FLN"
		send_dock "STATUS" "FLN"
	}

	method SetBuddyListPrivacy { privacy } {
		change_BLP_settings $privacy
	}

	method SetPersonalInformation {key value} {
		::abook::setPersonal $key $value
		# TODO this should go in the protocol, it should update its own capabilities...
		if { $key == "MOB" && $value == "Y"} {
			::MSN::setClientCap paging
		}
	}

	method SetUserInformation {username key value} {
		if {[string first "tel:" $value] == 0} {
			set value [string range $value [string length "tel:"] end]
		}
		::abook::setVolatileData $username $key $value
	}

	method SetUserPSM { username psm media } {
		::abook::setVolatileData $username PSM $psm
		::abook::setVolatileData $username currentMedia $media

		foreach chat_id [::ChatWindow::getAllChatIds] {
			if { $chat_id == $username } {
				::ChatWindow::TopUpdate $chat_id
			} else {
                        	foreach user_in_chat [::MSN::usersInChat $chat_id] {
	                                if { $user_in_chat == $username } {
	                                        ::ChatWindow::TopUpdate $chat_id
	                                        break
	                                }
	                        }
			}
                }
		# TODO this should become a 'data' layer event
		::Event::fireEvent contactPSMChange protocol $username
	}

	method AddUser { username nickname contactguid list_names groups } {
		# TODO OLD CODE

		::MSN::contactListChanged

		#Make list unconsistent while receiving contact lists
		::abook::unsetConsistent

		#Remove user from all lists while receiving List data
		::abook::setContactData $username lists ""

		::abook::setContactData $username nick $nickname

		::abook::setContactData $username contactguid $contactguid
		::abook::setContactForGuid $contactguid $username

		foreach list_sort $list_names {
			::abook::addContactToList $username $list_sort
			::MSN::addToList $list_sort $username

			#No need to set groups and set offline state if command is not in FL
			if { $list_sort == $FORWARD_LIST } {
				::abook::setContactData $username group $groups
				::abook::setVolatileData $username state $OFFLINE
			}
		}

		set lists [::abook::getLists $username]
		if { [lsearch $lists $PENDING_LIST] != -1 } {
			if { [lsearch [::abook::getLists $username] $ALLOW_LIST] != -1 || [lsearch [::abook::getLists $username] $BLOCK_LIST] != -1 } {
				#We already added it we only move it from PL to RL
				#Just add to RL for now and let the handler remove it from PL... to be sure it's the correct order...
				$protocol AddUser $username $REVERSE_LIST
			} else {
				newcontact $username $nickname
			}
		}

	}
	method AddGroup { groupid groupname } {
		# TODO OLD CODE
		# TODO this should creaet a new Group object
		::groups::Set $groupname $groupid
	}

	method Save { } {
		::abook::setConsistent
		::abook::saveToDisk		
	}

	method SetMyStatus { status } {	
		::MSN::setMyStatus $status
	}

	method SetMyDisplayPicture { msnobj } {	
		::abook::setVolatileData myself msnobj $msnobj
	}

	method SetMyPSM { psm media } {
		::abook::setPersonal PSM $psm
		::abook::setPersonal currentMedia $psm
	}

	method GetMyPSM {  } {
		return [::abook::getPersonal PSM]
	}

	method GetMyMedia { } {
		return [::abook::getPersonal currentMedia]
	}

	method GetMyNickname { } {
		return [::abook::getPersonal MFN]
	}

	method GetMyStatus { } {
		return [::MSN::myStatusIs]
	}

	method GetMyDisplayPicture { } {	
		return [::abook::getVolatileData myself msnobj]
	}
	method GetUserStatus { email } {
		return [::abook::getVolatileData $email state]
	}
	method SetUserStatus { email state } {
		return [::abook::setVolatileData $email state $state]
	}
	method GetUserNickname { email } {
		return [::abook::getNick $email]
	}
	method GetUserCapabilities { email } {
		return [::abook::getContactData $email clientid]
	}
	method GetUserDisplayPicture { email } {
		return [::abook::getVolatileData $email msnobj]
	}
	method GetUserPSM { email } {
		return	[::abook::getVolatileData $email PSM]
	}
	method GetUserMedia { email } {
		return [::abook::getVolatileData $email currentMedia]
	}
}