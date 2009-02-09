#!/bin/bash

# testing.sh - part of RHTS library
# Authors:  Petr Muller     <pmuller@redhat.com> 
#
# Description: Contains helpers for various testing tasks
#
# Copyright (c) 2008 Red Hat, Inc. All rights reserved. This copyrighted material 
# is made available to anyone wishing to use, modify, copy, or
# redistribute it subject to the terms and conditions of the GNU General
# Public License v.2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

: <<=cut
=pod

=head1 NAME

analyze.sh - RHTS lib functions for various testing tasks

=head1 DESCRIPTION

Contains helpers for various testing tasks

=head1 FUNCTIONS

=cut

. $RHTSLIB/logging.sh
. $RHTSLIB/journal.sh

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# rlDejaSum
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
: <<=cut
=pod

=head2 Analyze

=head3 rlDejaSum

TODO description

    rlDejaSum par1 par2

=over

=item par1

TODO description

=item par2

TODO description

=back

Return 0 if... TODO

=cut

rlDejaSum(){
	rlLog "Summarizing files: $1 $2"
	rlLogDebug "Calling $RHTSLIB/perl/deja-summarize routine"
	$RHTSLIB/perl/deja-summarize $1 $2 >> $OUTPUTFILE
}

rlCompareJournalWithRCW(){
	if [ -x /usr/bin/rcw-copy-log ]
	then
		jrnl=/tmp/rcw-journal
		rlJournalPrint > $jrnl
		rcw-copy-log $jrnl
		cp "/usr/share/rhts-library/python/journal-compare.py" compare.sh
		echo "compare.sh" > COMPARE-LIST
	else
		rlLogWarning "RCW files were not found on this system, doing nothing"
	fi
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUTHORS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
: <<=cut
=pod

=head1 AUTHORS

=over

=item *

Petr Muller <pmuller@redhat.com>

=item *

Jan Hutar <jhutar@redhat.com>

=item *

Petr Splichal <psplicha@redhat.com>

=back

=cut
