# this should deal with protocols, it's the one that should package require the different protocols available *when needed* and would give access to a protocol instance depending on the profile type (in case we support multiprotocol based on profile creation).

# for now we only require MSNP.
package require MSNP

snit::type ProtocolManager {

}