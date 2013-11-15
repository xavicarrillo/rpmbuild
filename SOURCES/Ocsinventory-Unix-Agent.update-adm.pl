#!/usr/bin/perl

use XML::Simple;

$file_url = '/var/lib/ocsinventory-agent/http:__inventory-1.domain.com_ocsinventory/ocsinv.adm';
$xml = new XML::Simple;
$data = $xml->XMLin($file_url,forcearray=>1,KeepRoot=>1);

$qasname=`/opt/quest/bin/vastool -u host/ attrs host/ | grep cn\: | cut -d\\  -f2`;
$qascontainer=`/opt/quest/bin/vastool -u host/ attrs host/ | grep distinguishedName\: | cut -d\\  -f2`;
chomp($qasname);
chomp($qascontainer);

for (@{$data->{ADM}[0]->{ACCOUNTINFO}}) {
        if ( $_->{KEYNAME}[0] eq 'fields_3' ) {
                $_->{KEYVALUE} = [$qasname];
        }
        if ($_->{KEYNAME}[0] eq 'fields_4') {
                $_->{KEYVALUE} = [$qascontainer];
        }
}

$xml->XMLout($data,
            KeepRoot   => 1,
            OutputFile => $file_url,
            XMLDecl    => "<?xml version='1.0'?>",
        );

