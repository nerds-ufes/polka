/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

const bit<16> TYPE_IPV4 = 0x800;
const bit<16> TYPE_SRCROUTING = 0x1234;


//Ethernet frame payload padding and P4
//https://github.com/p4lang/p4-spec/issues/587

/*************************************************************************
*********************** H E A D E R S  ***********************************
*************************************************************************/

typedef bit<9>  egressSpec_t;
typedef bit<48> macAddr_t;
typedef bit<32> ip4Addr_t;

header ethernet_t {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
}

header potPolka_t {
    bit<160>   routeId;
    bit<16>    rnd;
    bit<16>    cml;
}

header ipv4_t {
    bit<4>    version;
    bit<4>    ihl;
    bit<8>    diffserv;
    bit<16>   totalLen;
    bit<16>   identification;
    bit<3>    flags;
    bit<13>   fragOffset;
    bit<8>    ttl;
    bit<8>    protocol;
    bit<16>   hdrChecksum;
    ip4Addr_t srcAddr;
    ip4Addr_t dstAddr;
}

struct metadata {
    bit<160>   routeId;
    bit<16>    etherType;
    bit<1>     apply_sr;
    bit<9>     port;
    bit<16>    poly1;
    bit<16>    secret;
    bit<16>    mersenne;
    bit<4>     mersenne_b;
    bit<1>     verifyPOT;
    bit<16>    rnd;
    bit<16>    cml;
    bit<16>    prev_rnd;
    bit<16>    prev_cml;
    ip4Addr_t  ipAddr;
}

struct polka_t_top {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
    bit<160>    routeId;
}

struct headers {
    ethernet_t  ethernet;
    potPolka_t  potPolka;
    ipv4_t      ipv4;
}

/*************************************************************************
*********************** P A R S E R  ***********************************
*************************************************************************/

parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

    state start {
        transition parse_ethernet;
    }

    state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            TYPE_IPV4: parse_ipv4;
            TYPE_SRCROUTING: parse_srcRouting;
            default: accept;
        }
    }

    state parse_srcRouting {
        packet.extract(hdr.potPolka);
        transition accept;
    }

    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition accept;
    }


}


/*************************************************************************
************   C H E C K S U M    V E R I F I C A T I O N   *************
*************************************************************************/

control MyVerifyChecksum(inout headers hdr, inout metadata meta) {
    apply {  }
}


/*************************************************************************
**********************  T U N N E L   E N C A P   ************************
*************************************************************************/
control process_tunnel_encap(inout headers hdr,
                            inout metadata meta,
                            inout standard_metadata_t standard_metadata) {
    action tdrop() {
        mark_to_drop(standard_metadata);
    }

    action add_sourcerouting_header (   egressSpec_t port, bit<1> sr, macAddr_t dmac,
                                        bit<160>  routeIdPacket, bit<16> rnd, bit<16> cml){

        standard_metadata.egress_spec = port;
        meta.apply_sr = sr;
        meta.rnd = rnd;
        meta.cml = cml;

        hdr.ethernet.dstAddr = dmac;

        hdr.potPolka.setValid();
        hdr.potPolka.routeId = routeIdPacket;
    }

    table tunnel_encap_process_sr {
        key = {
            hdr.ipv4.dstAddr: lpm;
        }
        actions = {
            add_sourcerouting_header;
            tdrop;
        }
        size = 1024;
        default_action = tdrop();
    }

    apply {
        tunnel_encap_process_sr.apply();
        if(meta.apply_sr!=1){
            meta.prev_rnd = hdr.potPolka.rnd;
            meta.prev_cml = hdr.potPolka.cml;
            hdr.ethernet.etherType = TYPE_IPV4;
            hdr.potPolka.setInvalid();
            // if (45 == meta.prev_rnd && 55 == meta.prev_cml){
                standard_metadata.egress_spec = (bit<9>) 1;
            // }else{
                //  tdrop();
            // }       
        }else{
            hdr.ethernet.etherType = TYPE_SRCROUTING;
            hdr.potPolka.rnd = meta.rnd;
            hdr.potPolka.cml = meta.cml;
        }
    }

}


/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {

    action drop() {
        mark_to_drop(standard_metadata);
    }

    action calc_poly1(){
        //to calculate poly 1
        meta.poly1 = 0;
        meta.secret = 10;
    }


    apply {

    	// if (hdr.ipv4.isValid() && hdr.ethernet.etherType != TYPE_SRCROUTING) {
        //     process_tunnel_encap.apply(hdr, meta, standard_metadata);
        // } else if (hdr.ethernet.etherType == TYPE_SRCROUTING) {
        //     // process_tunnel_encap.apply(hdr, meta, standard_metadata);
        //     hdr.ethernet.etherType = TYPE_IPV4;
        //     hdr.potPolka.setInvalid();
        //     if (meta.rnd == meta.prev_rnd && meta.cml == meta.prev_cml){
        //         standard_metadata.egress_spec = 1;
        //     }else{
        //         drop();
        //     }
		// }

        // if (hdr.ipv4.isValid() && hdr.ethernet.etherType != TYPE_SRCROUTING) {
            process_tunnel_encap.apply(hdr, meta, standard_metadata);
        // } else if (hdr.ethernet.etherType == TYPE_SRCROUTING) {
            // process_tunnel_encap.apply(hdr, meta, standard_metadata);
            // hdr.ethernet.etherType = TYPE_IPV4;
            // hdr.potPolka.setInvalid();
            // if (meta.rnd == meta.prev_rnd && meta.cml == meta.prev_cml){
            //     standard_metadata.egress_spec = 1;
            // }else{
            //     drop();
            // }
		// }
    }
}



/*************************************************************************
****************  E G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {
    apply {  }
}

/*************************************************************************
*************   C H E C K S U M    C O M P U T A T I O N   **************
*************************************************************************/

control MyComputeChecksum(inout headers  hdr, inout metadata meta) {
    apply {  }
}

/*************************************************************************
***********************  D E P A R S E R  *******************************
*************************************************************************/

control MyDeparser(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.potPolka);
        packet.emit(hdr.ipv4);
    }
}

/*************************************************************************
***********************  S W I T C H  *******************************
*************************************************************************/

V1Switch(
    MyParser(),
    MyVerifyChecksum(),
    MyIngress(),
    MyEgress(),
    MyComputeChecksum(),
    MyDeparser()
) main;
