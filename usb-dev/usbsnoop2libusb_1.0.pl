#!/usr/bin/perl -w
# Please send any comments, bug reports or new ideas to timo.lindfors@iki.fi
# Please see http://iki.fi/lindi/usb/usbsnoop.txt for usage instructions.
# 2009-03-27/jucablues: Ported to libusb-1.0 (due to prior limit of 32kb in isoch transfers)
# 2007-11-25/lindi: URB_FUNCTION_CLEAR_FEATURE_TO_ENDPOINT
# 2006-01-07/lindi: ignore "non printable" URBs
# 2006-08-30/lindi: handle URB_FUNCTION_SELECT_INTERFACE, escape \0 in perl
# 2006-07-18/lindi: allow product id to be 0x0000
# 2006-03-09/lindi: don't fill buffer before reads
# 2005-09-18/lindi: parse transfer buffers properly
# 2005-12-24/lindi: 
use strict;

my ($line,$urb, $last_time);

my %endpointtype;

$last_time = 0;

my $maxIsoBufLength = 65536;

#set this to 1 if you wish to see the first bytes that originally came as response of isoch transfers in the logged USB activity:
my $show_received_bytes = 0;

my $usbsnoopbugseen = 0;

sub get_transferbuffer_contents {
    my (@lines) = @_;
    my $buffer = "";
    foreach my $line (@lines) {
	chomp($line);
	if ($line =~ /^    0[0-9a-f]{7}: ([^ ].+)/) {
	    my $bytes = $1;
	    $bytes =~ s/ /\\x/g;
	    $bytes =~ s/^/\\x/;
	    $buffer .= $bytes;
	}
    }
    return $buffer;
}

sub process_urb {
    my $text = shift;
    if (!defined($text)) {
	return;
    }
    my @lines = split(/\n/, $text);
    if ($text =~ m/UsbSnoop - incorrect UrbHeader.Length/) {
	print("/* usbsnoop bug detected */\n");
	$usbsnoopbugseen = 1;
    }
    if ($text =~ m/coming back/) {
		if ($show_received_bytes){
			if ($text =~ m/:((\s[a-f0-9][a-f0-9])+)/) {
				print "printf(\"received in the log: $1\\n\");\n";
			}
		}

		if ($text =~ m/URB_FUNCTION_SELECT_CONFIGURATION/) {
			my $endpoint;
			foreach my $line (@lines) {
			if ($line =~ /EndpointAddress *= 0x([a-f0-9]+)/) {
				$endpoint = $1;
			}
			if ($line =~ /PipeType *= 0x([a-f0-9]+) /) {
				my $pipetype = $1;
				$endpointtype{$endpoint} = $pipetype;
			}
		}
	} elsif (($usbsnoopbugseen == 1) and ($text =~ m/URB_FUNCTION_SELECT_INTERFACE/)) {
	    # UsbSnoop - incorrect UrbHeader.Length=0, should be at least 16
	    # and usbsnoop does not show what we sent! So, we need to parse
	    # alternate interface from the reply.
	    if ($text =~ m/Interface: AlternateSetting *= ([0-9]+)/) {
		my $AlternateSetting = $1;
		chomp($AlternateSetting);
		if ($text =~ /URB (\d+) /) {
		    my $urbnumber = $1;
		    chomp($urbnumber);
			print "ret = libusb_set_interface_alt_setting(devh,	0, $AlternateSetting);\n";
		    print "printf(\"$urbnumber set alternate setting returned %d\\n\", ret);\n";
		}
	    }
	    $usbsnoopbugseen = 0;
	}
	return;
    }
#    print "/*\n$text\n*/\n";

#	print '//printf("pressione qualquer tecla\n");';
#	print '//scanf("%s", useless_string);';
    my ($time, $TransferBufferLength, $DescriptorType, $Index, $bConfigurationValue, $Value, $Request, $endpoint, $urbnumber, $AlternateSetting, $FeatureSelector, $IsoPacket1Offset, $IsoPacketLastIndex);
    if ($text =~ m/(\d+) ms/) {
	$time = $1;
    }

    if ($last_time == 0) {
	$last_time = $time;
    } else {
	my $timediff = $time - $last_time;
	if ($timediff > 2500) {
	    #$timediff = 2500; # FIXME
	}
#	if ($timediff > 0) {
	    print "usleep($timediff*1000);\n";
#	}
	$last_time = $time;
    }
    if ($text =~ m/TransferBufferLength = 0([^ ]+)/) {
	$TransferBufferLength = $1;
	chomp($TransferBufferLength);
    }
    if ($text =~ m/DescriptorType *= 0([^ ]+)/) {
	$DescriptorType = $1;
	chomp($DescriptorType);
    }
    if ($text =~ m/Index *= 0([a-f0-9]+)/) {
	$Index = $1;
	chomp($Index);
    }
    if ($text =~ m/bConfigurationValue *= 0x0([^ ]+)/) {
	$bConfigurationValue = $1;
	chomp($bConfigurationValue);
    }
    if ($text =~ m/Value *= 0([^ ]+)/) {
	$Value = $1;
	chomp($Value);
    }
    if ($text =~ m/Request *= 0([^ ]+)/) {
	$Request = $1;
	chomp($Request);
    }
    if ($text =~ m/endpoint 0x([^ \]]+)/) {
	$endpoint = $1;
	chomp($endpoint);
    }
    if ($text =~ m/URB (\d+) /) {
	$urbnumber = $1;
	chomp($urbnumber);
    }
    if ($text =~ m/AlternateSetting *= ([0-9]+)/) {
	$AlternateSetting = $1;
	chomp($AlternateSetting);
    }
    if ($text =~ m/FeatureSelector *= ([0-9]+)/) {
	$FeatureSelector = $1;
	chomp($FeatureSelector);
    }
    if ($text =~ m/IsoPacket\[1\].Offset *= (\d+)/) {
	$IsoPacket1Offset = $1;
	chomp($IsoPacket1Offset);
    }
    foreach my $line (@lines) {
	if ($line =~ /IsoPacket\[(\d+)\]/) {
	    $IsoPacketLastIndex = $1;
	    chomp($IsoPacketLastIndex);
	}
    }
    if ($text =~ m/URB_FUNCTION_GET_DESCRIPTOR_FROM_DEVICE/) {
	print "ret = libusb_get_descriptor(devh, 0x$DescriptorType, 0x$Index, buf, 0x$TransferBufferLength);\n";
	print "printf(\"$urbnumber get descriptor returned %d, bytes: \\n \", ret);\n";
	print "print_bytes(buf, ret);\n";
	print "printf(\"\\n\");\n";
    } elsif ($text =~ m/URB_FUNCTION_GET_DESCRIPTOR_FROM_INTERFACE/) {
	printf "ret = libusb_get_descriptor(devh, 0x$DescriptorType, 0x$Index, buf, 0x$TransferBufferLength);\n";
	print "printf(\"$urbnumber get descriptor returned %d, bytes: \\n \", ret);\n";
	print "print_bytes(buf, ret);\n";
	print "printf(\"\\n\");\n";
    } elsif ($text =~ m/URB_FUNCTION_SELECT_CONFIGURATION/) {
	if (defined($bConfigurationValue)) {
	    print "ret = libusb_release_interface(devh, 0);\n";
	    print "if (ret != 0) printf(\"failed to release interface before set_configuration: %d\\n\", ret);\n";
	    print "ret = libusb_set_configuration(devh, 0x$bConfigurationValue);\n";
	    print "printf(\"$urbnumber set configuration returned %d\\n\", ret);\n";
	    print "ret = libusb_claim_interface(devh, 0);\n";
	    print "if (ret != 0) printf(\"claim after set_configuration failed with error %d\\n\", ret);\n";
	}
	if (defined($AlternateSetting)) {
		print "ret = libusb_set_interface_alt_setting(devh,	0, $AlternateSetting);\n";
	    print "printf(\"$urbnumber set alternate setting returned %d\\n\", ret);\n";
	}    
    } elsif ($text =~ m/URB_FUNCTION_CLASS_INTERFACE/) {
	my $requesttype = "LIBUSB_REQUEST_TYPE_CLASS + LIBUSB_RECIPIENT_INTERFACE";
	if ($text =~ m/USBD_TRANSFER_DIRECTION_IN/) {
	    $requesttype .= " + LIBUSB_ENDPOINT_IN";
	}
	my $bytes = get_transferbuffer_contents(@lines);
	if ($bytes ne "") {
	    print "memcpy(buf, \"$bytes\", 0x$TransferBufferLength);\n";
	}
	print "ret = libusb_control_transfer(devh, $requesttype, 0x$Request, 0x$Value, 0x$Index, buf, 0x$TransferBufferLength, 1000);\n";

	if ($text =~ m/USBD_TRANSFER_DIRECTION_IN/) {
	    print "printf(\"$urbnumber control msg returned %d, bytes: \\n \", ret);\nprint_bytes(buf, ret);\n";
	} else {
	    print "printf(\"$urbnumber control msg returned %d\", ret);\n";
	}
	print "printf(\"\\n\");\n";
    } elsif ($text =~ m/URB_FUNCTION_VENDOR_INTERFACE/) {
	my $requesttype = "LIBUSB_REQUEST_TYPE_VENDOR + LIBUSB_RECIPIENT_INTERFACE";
	if ($text =~ m/USBD_TRANSFER_DIRECTION_IN/) {
	    $requesttype .= " + LIBUSB_ENDPOINT_IN";
	}
	my $bytes = get_transferbuffer_contents(@lines);
	if ($bytes ne "") {
	    print "memcpy(buf, \"$bytes\", 0x$TransferBufferLength);\n";
	}
	print "ret = libusb_control_transfer(devh, $requesttype, 0x$Request, 0x$Value, 0x$Index, buf, 0x$TransferBufferLength, 1000);\n";
	print "printf(\"$urbnumber control msg returned %d, bytes: \\n \", ret);\n";
	print "print_bytes(buf, ret);\n";
	print "printf(\"\\n\");\n";
    } elsif ($text =~ m/URB_FUNCTION_BULK_OR_INTERRUPT_TRANSFER/) {
	my $method;
	if ( ( hex $endpoint & 128 ) == 128 ) {
	    # if ($text =~ /USBD_TRANSFER_DIRECTION_IN/) {
	    $method = "read";
	} else {
	    $method = "write";
	}
	my $type = $endpointtype{$endpoint};
	if (!defined($type)) {
	    die "can't find \"$endpoint\"\n";
	}
	my $mode;
	if ($type eq "00000002") {
	    $mode = "bulk";
	} elsif ($type eq "00000003") {
	    $mode = "interrupt";
	} else {
	    die "unrecognised endpointtype \"$type\" for endpoint \"$endpoint\"";
	}
	my $bytes = get_transferbuffer_contents(@lines);
	if ($bytes ne "" and $method eq "write") {
	    print "memcpy(buf, \"$bytes\", 0x$TransferBufferLength);\n";
	}
	my $timeout = 1000;
	if ($mode eq "bulk" and hex($TransferBufferLength) > 50) {
	    $timeout = 1000 + hex($TransferBufferLength) * 0.06;
	    $timeout = sprintf("%.0d", $timeout); # round to integer
	}
	print "ret = usb_".$mode."_$method(devh, 0x$endpoint, buf, 0x$TransferBufferLength, $timeout);\n";
	print "printf(\"$urbnumber $mode $method returned %d, bytes: \\n \", ret);\n";
# sounds weird but write requests can actually also return data
#	if ($method eq "read") {
	    print "print_bytes(buf, ret);\n";
#	}
	print "printf(\"\\n\");\n";
    } elsif ($text =~ m/URB_FUNCTION_SET_FEATURE_TO_DEVICE/) {
	my $requesttype = "LIBUSB_REQUEST_TYPE_STANDARD + LIBUSB_RECIPIENT_DEVICE";
	print "ret = libusb_control_transfer(devh, $requesttype, USB_REQ_SET_FEATURE, $FeatureSelector, 0, buf, 0, 1000);\n";
	print "printf(\"$urbnumber set feature request returned %d\\n\", ret);\n";
    } elsif ($text =~ m/URB_FUNCTION_VENDOR_DEVICE/) {
	my $requesttype = "LIBUSB_REQUEST_TYPE_VENDOR + LIBUSB_RECIPIENT_DEVICE";
	if ($text =~ m/USBD_TRANSFER_DIRECTION_IN/) {
	    $requesttype .= " + LIBUSB_ENDPOINT_IN";
	}
	my $bytes = get_transferbuffer_contents(@lines);
	if ($bytes ne "") {
	    print "memcpy(buf, \"$bytes\", 0x$TransferBufferLength);\n";
	}
	print "ret = libusb_control_transfer(devh, $requesttype, 0x$Request, 0x$Value, 0x$Index, buf, 0x$TransferBufferLength, 1000);\n";
	print "printf(\"$urbnumber control msg returned %d, bytes: \\n \", ret);\n";
	print "print_bytes(buf, ret);\n";
	print "printf(\"\\n\");\n";
    } elsif ($text =~ m/URB_FUNCTION_GET_CURRENT_FRAME_NUMBER/) {
	my $requesttype = "LIBUSB_REQUEST_TYPE_VENDOR + LIBUSB_RECIPIENT_DEVICE";
	# TODO
    } elsif ($text =~ m/URB_FUNCTION_ISOCH_TRANSFER/) {
	if (!defined($IsoPacket1Offset)) {
	    die "can't find offset of first iso packet\n";
	}
	if (!defined($IsoPacketLastIndex)) {
	    die "can't find index of last iso packet\n";
	}
	my $packetsize = $IsoPacket1Offset;
	my $packetcount = $IsoPacketLastIndex + 1;
	if ($packetcount * $packetsize > $maxIsoBufLength) {
	    die "packetcount ($packetcount) or packetsize ($packetsize) is way too large!\nMaybe you could increase the \$maxIsoBufLength parameter in usbsnoop2libusb_1.0.pl\n";
	}
	print "transfer = libusb_alloc_transfer($packetcount);\n";
	print "libusb_fill_iso_transfer(transfer, devh, 0x$endpoint, isobuf, $packetsize * $packetcount, $packetcount, iso_callback, NULL, 10000);\n";
	print "ret = libusb_submit_transfer(transfer);\n";
	print "if (ret) printf(\"$urbnumber isochronous submit returned %d\\n\", ret);\n";
	# TODO
    } elsif ($text =~ m/URB_FUNCTION_CLEAR_FEATURE_TO_ENDPOINT/) {
		my $requesttype = "LIBUSB_REQUEST_TYPE_STANDARD + LIBUSB_RECIPIENT_ENDPOINT";
		print "ret = libusb_control_transfer(devh, $requesttype, LIBUSB_REQUEST_CLEAR_FEATURE, $FeatureSelector, 0, buf, 0, 1000);\n";
		print "printf(\"$urbnumber clear feature request returned %d\\n\", ret);\n";
    } elsif ($text =~ m/URB_FUNCTION_ABORT_PIPE/) {
	# TODO: implement

	#	my $requesttype = "LIBUSB_REQUEST_TYPE_STANDARD + LIBUSB_RECIPIENT_ENDPOINT";
	#	print "ret = libusb_control_transfer(devh, $requesttype, LIBUSB_REQUEST_CLEAR_FEATURE, $FeatureSelector, 0, buf, 0, 1000);\n";
	#	print "printf(\"$urbnumber clear feature request returned %d\\n\", ret);\n";

		print "printf(\"$urbnumber testing abort pipe implementation :P\\n\");\n";
    } elsif ($text =~ m/URB_FUNCTION_RESET_PIPE/) {
	# TODO: implement
	print "printf(\"$urbnumber reset pipe not implemented yet :(\\n\");\n";
    } elsif ($text =~ m/URB_FUNCTION_SELECT_INTERFACE/) {
        if (!defined($AlternateSetting)) {
            die "can't find alternatesetting\n";
        }
		print "ret = libusb_set_interface_alt_setting(devh,	0, $AlternateSetting);\n";
        print "printf(\"$urbnumber set alternate setting returned %d\\n\", ret);\n";
    } elsif ($text =~ m/incorrect UrbHeader.Length=0,/) {
	# ignore
    } elsif ($text =~ m/non printable URB with function code 0x0000002a/) {
	print("/* usbsnoop says URB is non prinbable! */");
    } else {
	die "unrecognized URB type, text = \"$text\"";
    }
}


print <<EOF
/* This file is generated with usbsnoop2libusb_1.0.pl from a usbsnoop log file. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <libusb-1.0/libusb.h>

void print_bytes(char *bytes, int len) {
    int i;
    if (len > 0) {
	for (i=0; i<len; i++) {
	    printf("%02x ", (int)((unsigned char)bytes[i]));
	}
	printf("\\"");
        for (i=0; i<len; i++) {
	    printf("%c", isprint(bytes[i]) ? bytes[i] : '.');
        }
        printf("\\"");
    }
}

static void iso_callback(struct libusb_transfer *transfer){
	int i;
	int buf_index=0;
	for (i = 0; i < transfer->num_iso_packets; i++) {
	struct libusb_iso_packet_descriptor *desc =  &transfer->iso_packet_desc[i];
		unsigned char *pbuf = transfer->buffer + buf_index;
		buf_index+=desc->length;
		if (desc->actual_length != 0) {
			printf("isopacket %d received %d bytes:\\n", i, desc->actual_length);
			print_bytes(pbuf, desc->actual_length);
		}
	}
	libusb_free_transfer(transfer);
}

int main(int argc, char **argv) {
    int ret, vendor, product;
	char buf[65535];
	char isobuf[$maxIsoBufLength];
	static struct libusb_device_handle *devh = NULL;
	struct libusb_transfer* transfer;

    if (argc!=3) {
	printf("usage: %s vendorID productID\\n", argv[0]);
	exit(1);
    }

    char *endptr;
    vendor = strtol(argv[1], &endptr, 16);
    if (*endptr != '\\0') {
	printf("invalid vendor id\\n");
	exit(1);
    }
    product = strtol(argv[2], &endptr, 16);
    if (*endptr != '\\0') {
	printf("invalid product id\\n");
	exit(1);
    }


	ret = libusb_init(NULL);
	if (ret < 0)
		return ret;
	
    libusb_set_debug(NULL, 3);
	devh = libusb_open_device_with_vid_pid(NULL, vendor, product);

EOF
    ;

while (defined($line = <>)) {
    if ($line =~ m/ URB (\d+) (going down|coming back)/) {
        &process_urb($urb);
        $urb = $line;
    } elsif (defined($urb)) {
        $urb .= $line;
    }
}

&process_urb($urb);

print <<EOF
	libusb_close(devh);
	libusb_exit(NULL);
	return 0;
}
EOF
    ;
