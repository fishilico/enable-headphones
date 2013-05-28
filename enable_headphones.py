#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""Enable speakers for my sound card

With HDA Analyser program, EAPD is turned off whenever the speaker ext jack is
plugged. Re-enable it to have sound !
"""

import sys

from hda_analyzer import hda_codec

# Static configuration (card, codec, node)
CONFIG_NODE = (0, 0, 0x25)


def get_codec(card_index, codec_index):
    """Retrieve a codec given indexes"""
    try:
        return hda_codec.HDACodec(card_index, codec_index)
    except OSError as msg:
        if msg[0] == 13:
            print("Codec %i/%i unavailable - permissions..." %
                (card_index, codec_index))
        elif msg[0] == 16:
            print("Codec %i/%i is busy..." %
                (card_index, codec_index))
        elif msg[0] != 2:
            print("Codec %i/%i access problem (%s)" %
                (card_index, codec_index, repr(msg)))
    return


def main(node=None):
    """Entry point, tweak settings of a given node"""
    node = node or CONFIG_NODE
    (card_index, codec_index, node_index) = node
    codec = get_codec(card_index, codec_index)
    if codec is None:
        return 1

    codec.analyze()
    try:
        node = codec.nodes[node_index]
    except KeyError:
        print("Unable to find node in codec")
        return 1

    print("Codec %i/%i" % (card_index, codec_index))
    print(codec.dump_node(node))

    # Sanity check
    assert(node.jack_type_name == 'HP Out')
    assert(node.jack_location_name == 'Ext')
    assert(node.jack_conn_name == 'Jack')

    # node.pincap_eapdbtls = 2
    # node.pinctls = 0xc0
    changed = node.eapdbtl_set_value('EAPD', True)
    changed = node.pin_widget_control_set_value('HP', True) or changed
    changed = node.pin_widget_control_set_value('OUT', True) or changed
    if changed:
        print("Changes were done in EAPD and pin-ctls. Here is the new state")
        print(codec.dump_node(node))
    else:
        print("Nothing changed, EAPD and pinctl were already set")
    return 0


if __name__ == '__main__':
    sys.exit(main())
