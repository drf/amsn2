
snit::type ClientID {

	typevariable mobile [expr {0x00000001}]
	typevariable inkgif [expr {0x00000004}]
	typevariable inkisf [expr {0x00000008}]
	typevariable webcam [expr {0x00000010}]
	typevariable multip [expr {0x00000020}]
	typevariable paging [expr {0x00000040}]
	typevariable drctpg [expr {0x00000080}]
	typevariable webmsn [expr {0x00000200}]
	typevariable tgw    [expr {0x00000800}]
	typevariable space  [expr {0x00001000}]
	typevariable mce    [expr {0x00002000}]
	typevariable direct [expr {0x00004000}]
	typevariable winks  [expr {0x00008000}]
	typevariable search [expr {0x00010000}]
	typevariable bot    [expr {0x00020000}]
	typevariable voice  [expr {0x00040000}]
	typevariable secure [expr {0x00080000}]
	typevariable sip    [expr {0x00100000}]
	typevariable shared [expr {0x00400000}]
	typevariable msnc1  [expr {0x10000000}]
	typevariable msnc2  [expr {0x20000000}]
	typevariable msnc3  [expr {0x30000000}]
	typevariable msnc4  [expr {0x40000000}]
	typevariable msnc5  [expr {0x50000000}]
	typevariable msnc6  [expr {0x60000000}]
	typevariable msnc7  [expr {0x70000000}]
	typevariable msnc   [expr {0xF0000000}]


	# set a capability of the client
	# possiblities for cap are:
	# mobile Mobile Device
	# inkgif receive Ink as gif
	# inkisf receive Ink as ISF
	# webcam Webcam
	# multip Multi-Packeting
	# paging Paging
	# drctpg Direct-Paging
	# webmsn WebMessenger
	# tgw    Connected via TGW
	# space  User has an MSN Spaces
	# mce    Connected using Win XP Media Center Edition
	# direct DirectIM
	# winks  Winks
	# search Client supports Shared search
	# bot    Is Bot
	# voice  Client supports Voice Clips
	# secure Client supports secure channel chatting
	# sip    Client supports SIP based communiation
        # shared Client supports Shared Folders
	# msnc1  This is the value for MSNC1 (MSN Msgr 6.0)
	# msnc2  This is the value for MSNC2 (MSN Msgr 6.1)
	# msnc3  This is the value for MSNC3 (MSN Msgr 6.2)
	# msnc4  This is the value for MSNC4 (MSN Msgr 7.0)
	# msnc5  This is the value for MSNC5 (MSN Msgr 7.5)
	# msnc6  This is the value for MSNC5 (MSN Msgr 8.0)
	# msnc7  This is the value for MSNC5 (MSN Msgr 8.1)
	#
	#switch==1 means turn on, 0 means turn off 
	#
        # Reference : http://zoronax.spaces.live.com/?_c11_BlogPart_FullView=1&_c11_BlogPart_blogpart=blogview&_c=BlogPart&partqs=amonth%3d6%26ayear%3d2006
	#
	# From http://forums.fanatic.net.nz/index.php?showtopic=17639 thanks to Ole Andre 
	#define CapabilityMobileOnline 0x00000001
	#define CapabilityMSN8User 0x00000002
	#define CapabilityRendersGif 0x00000004
	#define CapabilityRendersIsf 0x00000008
	#define CapabilityWebCamDetected 0x00000010
	#define CapabilitySupportsChunking 0x00000020
	#define IsMobileEnabled 0x00000040
	#// FIXME: the canonical meaning of 0x00000080 is missing
	#define CapabilityWebIMClient 0x00000200
	#define CapabiltiyConnectedViaTGW 0x00000800
	#// FIXME: the canonical meaning of 0x00001000 is missing
	#define CapabilityMCEUser 0x00002000
	#define CapabilitySupportsDirectIM 0x00004000
	#define CapabilitySupportsWinks 0x00008000
	#define CapabilitySupportsSharedSearch 0x00010000
	#define CapabilityIsBot 0x00020000
	#define CapabilitySupportsVoiceIM 0x00040000
	#define CapabilitySupportsSChannel 0x00080000
	#define CapabilitySupportsSipInvite 0x00100000
	#define CapabilitySupportsSDrive 0x00400000
	#define CapabilityHasOnecare 0x01000000
	#define CapabilityP2PSupportsTurn 0x02000000
	#define CapabilityP2PBootstrapViaUUN 0x04000000
	#define CapabilityMsgrVersion 0xf0000000
	#define CapabilityP2PAware(id) ((id & CapabilityMsgrVersion) != 0)

	method setClientCap { cap { switch 1 } } {
		set clientid [::config::getKey clientid 0]

		if $switch {
			switch $cap {
				mobile { set clientid [expr {$clientid | 0x000001} ] }
				inkgif { set clientid [expr {$clientid | 0x000004} ] }
				inkisf { set clientid [expr {$clientid | 0x000008} ] }
				webcam { set clientid [expr {$clientid | 0x000010} ] }
				multip { set clientid [expr {$clientid | 0x000020} ] }
				paging { set clientid [expr {$clientid | 0x000040} ] }
				drctpg { set clientid [expr {$clientid | 0x000080} ] }
				webmsn { set clientid [expr {$clientid | 0x000200} ] }
				tgw    { set clientid [expr {$clientid | 0x000800} ] }
				space  { set clientid [expr {$clientid | 0x001000} ] }
				mce    { set clientid [expr {$clientid | 0x002000} ] }
				direct { set clientid [expr {$clientid | 0x004000} ] }
				winks  { set clientid [expr {$clientid | 0x008000} ] }
				search { set clientid [expr {$clientid | 0x010000} ] }
				bot    { set clientid [expr {$clientid | 0x020000} ] }
				voice  { set clientid [expr {$clientid | 0x040000} ] }
				secure { set clientid [expr {$clientid | 0x080000} ] }
				sip    { set clientid [expr {$clientid | 0x100000} ] }
				shared { set clientid [expr {$clientid | 0x400000} ] }
				msnc1  { set clientid [expr {$clientid | 0x10000000} ] }
				msnc2  { set clientid [expr {$clientid | 0x20000000} ] }
				msnc3  { set clientid [expr {$clientid | 0x30000000} ] }
				msnc4  { set clientid [expr {$clientid | 0x40000000} ] }
				msnc5  { set clientid [expr {$clientid | 0x50000000} ] }
				msnc6  { set clientid [expr {$clientid | 0x60000000} ] }
				msnc7  { set clientid [expr {$clientid | 0x70000000} ] }
			}
		} else {
			switch $cap {
				mobile { set clientid [expr {$clientid & (0xFFFFFFFF ^ 0x000001)} ] }
				inkgif { set clientid [expr {$clientid & (0xFFFFFFFF ^ 0x000004)} ] }
				inkisf { set clientid [expr {$clientid & (0xFFFFFFFF ^ 0x000008)} ] }
				webcam { set clientid [expr {$clientid & (0xFFFFFFFF ^ 0x000010)} ] }
				multip { set clientid [expr {$clientid & (0xFFFFFFFF ^ 0x000020)} ] }
				paging { set clientid [expr {$clientid & (0xFFFFFFFF ^ 0x000040)} ] }
				drctpg { set clientid [expr {$clientid & (0xFFFFFFFF ^ 0x000080)} ] }
				webmsn { set clientid [expr {$clientid & (0xFFFFFFFF ^ 0x000200)} ] }
				tgw    { set clientid [expr {$clientid & (0xFFFFFFFF ^ 0x000800)} ] }
				space  { set clientid [expr {$clientid & (0xFFFFFFFF ^ 0x001000)} ] }
				mce    { set clientid [expr {$clientid & (0xFFFFFFFF ^ 0x002000)} ] }
				direct { set clientid [expr {$clientid & (0xFFFFFFFF ^ 0x004000)} ] }
				winks  { set clientid [expr {$clientid & (0xFFFFFFFF ^ 0x008000)} ] }
				search { set clientid [expr {$clientid & (0xFFFFFFFF ^ 0x010000)} ] }
				bot    { set clientid [expr {$clientid & (0xFFFFFFFF ^ 0x020000)} ] }
				voice  { set clientid [expr {$clientid & (0xFFFFFFFF ^ 0x040000)} ] }
				secure { set clientid [expr {$clientid & (0xFFFFFFFF ^ 0x080000)} ] }
				sip    { set clientid [expr {$clientid & (0xFFFFFFFF ^ 0x100000)} ] }
				shared { set clientid [expr {$clientid & (0xFFFFFFFF ^ 0x400000)} ] }
				msnc1  { set clientid [expr {$clientid & (0xFFFFFFFF ^ 0x10000000)} ] }
				msnc2  { set clientid [expr {$clientid & (0xFFFFFFFF ^ 0x20000000)} ] }
				msnc3  { set clientid [expr {$clientid & (0xFFFFFFFF ^ 0x30000000)} ] }
				msnc4  { set clientid [expr {$clientid & (0xFFFFFFFF ^ 0x40000000)} ] }
				msnc5  { set clientid [expr {$clientid & (0xFFFFFFFF ^ 0x50000000)} ] }
				msnc6  { set clientid [expr {$clientid & (0xFFFFFFFF ^ 0x60000000)} ] }
				msnc7  { set clientid [expr {$clientid & (0xFFFFFFFF ^ 0x70000000)} ] }
			}
		}
		::config::setKey clientid $clientid
		return $clientid
	}
	method add_Clientid {chatid clientid} {

		##First save the clientid (number)
		::abook::setContactData $chatid clientid $clientid
		
		##Find out how the client-program is called
		switch [expr {$clientid & 0xF0000000}] {
			268435456 {
				# 0x10000000
				set clientname "MSN 6.0"
			}
			536870912 {
				# 0x20000000
				set clientname "MSN 6.1"
			}
			805306368 {
				# 0x30000000
				set clientname "MSN 6.2"
			}
			1073741824 {
				# 0x40000000
				set clientname "MSN 7.0"
			}
			1342177280 {
				# 0x50000000
				set clientname "MSN 7.5"
			}
			1610612736 {
				# 0x60000000
				set clientname "Windows Live Messenger 8.0"
			}
			1879048192 {
				# 0x70000000
				set clientname "Windows Live Messenger 8.1"
			}
			default {
				if {($clientid & 0x200) == [expr {0x200}]} {
                                set clientname "Webmessenger"
				} elseif {($clientid & 0x800) == [expr {0x800}]} {
					set clientname "Microsoft Office gateway"
				} else {
					set clientname "[trans unknown]"
				}
			}
			
		}	
		
		##Store the name of the client this user uses in the adressbook
		::abook::setContactData $chatid client $clientname

		
		
		##Set the capability flags for this user##
		
		set flags [list [list 1 mobile_device] [list 4 receive_ink] [list 8 sendnreceive_ink] [list 16 webcam_shared] [list 32 multi_packet] [list 64 msn_mobile] [list 128 msn_direct] [list 16384 directIM ] [list 32768 winks] ]
		
		foreach flag $flags {
			set bit [lindex $flag 0]
			set flagname [lindex $flag 1]
			#check if this bit is on in the clientid, ifso set it's flag
			if {($clientid & $bit) == $bit} {
				::abook::setContactData $chatid $flagname 1
			} else {
				::abook::setContactData $chatid $flagname 0
		}
		}		
		
	}
}
