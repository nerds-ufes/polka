/* -- P4_16 -- */
#include <core.p4>
#include <v1model.p4>

const bit<16> TYPE_IPV4 = 0x800;
const bit<16> TYPE_SRCROUTING = 0x1234;

/*************************
******** H E A D E R S  ************
*************************/

typedef bit<9>  egressSpec_t;
typedef bit<48> macAddr_t;
typedef bit<32> ip4Addr_t;
typedef bit<16> rnd_t;
typedef bit<16> cml_t;
typedef bit<16> mersenne_t;
typedef bit<4> mersenne_b_t;
typedef bit<16> x_t;
typedef bit<16> y_t;
typedef bit<16> lpc_t;
typedef bit<16> poly2_t;
typedef bit<4> pot_k_t;


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
    bit<160>  routeId;
    bit<16>   etherType;
    bit<1> apply_sr;
    bit<1> apply_decap;
    bit<9> port;
    poly2_t poly2;
    lpc_t lpc;
    rnd_t new_rnd;
    cml_t new_cml;
    x_t x;
    y_t y;
    mersenne_t mersenne;
    mersenne_b_t mersenne_b;
    pot_k_t pot_k;
}

struct polka_t_top {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
    bit<160>   routeId;
}

struct headers {
    ethernet_t  ethernet;
    potPolka_t  potPolka;
    ipv4_t      ipv4;
}

/*************************
******** P A R S E R  ************
*************************/

parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

    state start {
        meta.apply_sr = 0;
        transition verify_ethernet;
    }

    state verify_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            TYPE_SRCROUTING: get_routeId;
            default: accept;
        }
    }

    state get_routeId {
		meta.apply_sr = 1;
        packet.extract(hdr.potPolka);
        transition accept;
    }

}


/*************************
****   C H E C K S U M    V E R I F I C A T I O N   *****
*************************/

control MyVerifyChecksum(inout headers hdr, inout metadata meta) {
    apply {  }
}


/*************************
*****  I N G R E S S   P R O C E S S I N G   ********
*************************/

control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {
    action drop() {
        mark_to_drop(standard_metadata);
    }

    action srcRoute_nhop() {

        bit<16> nbase=0;
        bit<64> ncount=4294967296*2;
        bit<16> nresult;
        bit<16> nport;

        bit<160>routeid = (bit<160>) hdr.potPolka.routeId;

        bit<160>ndata = routeid >> 16;
        bit<16> dif = (bit<16>) (routeid ^ (ndata << 16));

        hash(
          nresult,
          HashAlgorithm.crc16_custom,
          nbase,
          {ndata},ncount
        );

        nport = nresult ^ dif;
        meta.pot_k = nport[12:9];
        meta.port = nport[8:0];
    }

    action initialize_param (
        x_t x, 
        y_t y, 
        lpc_t lpc, 
        mersenne_t mersenne, 
        mersenne_b_t mersenne_b, 
        poly2_t poly2
    ){
        meta.x = x;
        meta.y = y;
        meta.lpc = lpc;
        meta.mersenne = mersenne;
        meta.mersenne_b = mersenne_b;
        meta.poly2 = poly2;
    }
    
    table pot_param {
        key = {
            meta.pot_k: exact;
        }
        actions = {
            initialize_param;
            drop;
        }
        size = 128;
        default_action = drop();
    }

    action calc_cml(){
        meta.new_cml = (meta.y + meta.poly2) * meta.lpc;
        meta.new_cml = (meta.new_cml & meta.mersenne) + (meta.new_cml >> meta.mersenne_b);
    }
    // register<bit<16>>(32w2) debug;
    apply {
      if (meta.apply_sr==1){
        // POT pipeline
        // to calculate by using LPC
        srcRoute_nhop();
        pot_param.apply();
        calc_cml();
        if (meta.new_cml > meta.mersenne){
            meta.new_cml = meta.new_cml - meta.mersenne;
        }
        meta.new_cml = hdr.potPolka.cml + meta.new_cml;
        hdr.potPolka.cml = meta.new_cml;
          // PolKA's calculation
        standard_metadata.egress_spec = meta.port;
      }else{
        drop();
      }
    }
  }

/*************************
******  E G R E S S   P R O C E S S I N G   *******
*************************/

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {
    apply {  }
}

/*************************
*****   C H E C K S U M    C O M P U T A T I O N   ******
*************************/

control MyComputeChecksum(inout headers  hdr, inout metadata meta) {
    apply {  }
}

/*************************
********  D E P A R S E R  ************
*************************/

control MyDeparser(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.potPolka);
    }
}

/*************************
********  S W I T C H  ************
*************************/

V1Switch(
    MyParser(),
    MyVerifyChecksum(),
    MyIngress(),
    MyEgress(),
    MyComputeChecksum(),
      MyDeparser()
) main;
