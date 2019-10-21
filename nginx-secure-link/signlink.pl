#!/usr/bin/env perl

use utf8;
use strict;
use warnings;

#
# Perl implementation to generate hashed urls for nginx' secure_link module.
#

use Digest::MD5 qw(md5_base64);

# Achtung: Im Gegensatz zu den hashlink.* Beispielen ist der gesamte Link
#          Teil des zu signierenden Payloads, nicht nur der Dateiname am Ende.
my $prefix = "http://localhost:9005";
my $link = "/s/trade-secrets.txt";
my $secret = "secret";

# Lokale Zeit + 1 Tag
my $expires = int(time + 86400);

# Abgleichen mit secure_link_md5
my $url_hash = "${expires}${link} ${secret}";

$url_hash = md5_base64($url_hash);
$url_hash =~ s/\+/-/g;
$url_hash =~ s/\//_/g;
$url_hash =~ s/=//g;

my $final_url = "${prefix}${link}?md5=${url_hash}&expires=${expires}";
print($final_url . "\n");
