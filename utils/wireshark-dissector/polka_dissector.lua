--    This program is free software: you can redistribute it and/or modify
--    it under the terms of the GNU General Public License as published by
--    the Free Software Foundation, either version 3 of the License, or
--    (at your option) any later version.
--
--    This program is distributed in the hope that it will be useful,
--    but WITHOUT ANY WARRANTY; without even the implied warranty of
--    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
--    GNU General Public License for more details.
--
--    You should have received a copy of the GNU General Public License
--    along with this program.  If not, see <https://www.gnu.org/licenses/>.


-- create polka proto protocol and its fields
polka_proto = Proto ("polka","PolKA")
local version = ProtoField.uint8("version.addr", "Version", base.DEC)
local ttl = ProtoField.uint8("ttl.addr", "TTL", base.DEC)
local type = ProtoField.uint16("type.addr", "Type", base.HEX)
local routeid = ProtoField.guid("routeid", "Routeid")
local f_data = ProtoField.string("polkaproto.data", "Data", FT_STRING)

polka_proto.fields = {version, ttl, type, routeid}

proto_handle = Dissector.get("ip")

-- polkaproto dissector function
function polka_proto.dissector (buf, pkt, root)
  -- validate packet length is adequate, otherwise quit
  pkt.cols.protocol = polka_proto.name
  -- create subtree for polkaproto
  subtree = root:add(polka_proto, buf(0,20),"PolKA Header")
  -- add protocol fields to subtree
  subtree:add(version, buf(0,1)):append_text(" :Version of PolKA")
  subtree:add(ttl, buf(1,1)):append_text(" :Time to Live")
  subtree:add(type, buf(2,2)):append_text(" :Type of Next Protocol")
  subtree:add(routeid, buf(4,16)):append_text(" :Route ID")
  subtree:append_text(" Protocol")
  

proto_handle:call(buf:range(20):tvb(),pkt,root)
end

-- Initialization routine
function polka_proto.init()
end

-- subscribe for Ethernet packets on type 34882 (0x8842).
local eth_table = DissectorTable.get("ethertype")
eth_table:add(34882, polka_proto)