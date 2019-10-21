#!/usr/bin/env perl

use utf8;
use strict;
use warnings;

#
# Perl implementation to generate hashed urls for nginx' secure_link module.
#

require Digest::MD5;

my $prefix = "http://localhost:9005/p";
my $link = "trade-secrets.txt";
my $secret = "secret";

my $link_hash = Digest::MD5::md5_hex("${link}${secret}");

print("${prefix}/${link_hash}/${link}\n");
