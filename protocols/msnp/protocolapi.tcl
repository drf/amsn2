snit::type ProtocolAPI {
	option -protocol -default "" -configuremethod ConfigureProtocol
	variable protocol ""

	constructor { args } {
		::Events::registerEvent AddUser all all [list $self AddUser]
	}

	method ConfigureProtocol { opt value } {
		set options($opt) $value
		set protocol $value
	}

	method AddUser { email } {
		if {$protocol != "" } {
			$protocol AddUser $email
		}
	}

	method AddUserToGroup { email group} {
		if {$protocol != "" } {
			$protocol  AddUserToGroup $email $group
		}
	}

	method DeleteUser { email } {
		if {$protocol != "" } {
			$protocol DeleteUser $email
		}
	}

	method DeleteUserFromGroup { email group} {
		if {$protocol != "" } {
			$protocol DeleteUserFromGroup $email $group
		}

	}

	method AcceptUser { email } {
		if {$protocol != "" } {
			$protocol AcceptUser $email
		}
		
	}

	method BlockUser { email } {
		if {$protocol != "" } {
			$protocol BlockUser $email
		}

	}
	
	method UnBlockUser { email } {
		if {$protocol != "" } {
			$protocol UnBlockUser $email
		}
	
	}

	method DownloadUserDisplayPicture { email } {
		if {$protocol != "" } {
			$protocol DownloadUserDisplayPicture $email
		}
		
	}

	method AddGroup { name } {
		if {$protocol != "" } {
			$protocol AddGroup $name
		}
		
	}

	method DeleteGroup { group } {
		if {$protocol != "" } {
			$protocol DeleteGroup $group
		}
		
	}

	method RenameGroup { group name } {
		if {$protocol != "" } {
			$protocol RenameGroup $group $name
		}
		
	}

	method ChangeNickname { nick } {
		if {$protocol != "" } {
			$protocol ChangeNickname $nick 
		}
	}
	method ChangePSM { psm media} {
		if {$protocol != "" } {
			$protocol ChangePSM $psm $media
		}
	}
	method ChangeStatus { status } {
		if {$protocol != "" } {
			$protocol ChangeStatus $status 
		}
	}
}