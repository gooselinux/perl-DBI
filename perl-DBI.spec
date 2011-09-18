Name:           perl-DBI
Version:        1.609
Release:        4%{?dist}
Summary:        A database access API for perl

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://dbi.perl.org/
Source0:        http://www.cpan.org/authors/id/T/TI/TIMB/DBI-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl(ExtUtils::MakeMaker), perl(Test::Pod)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# The automated scripts are not able to get the version for this:
Provides:	perl(DBI) = %{version}

%description 
DBI is a database access Application Programming Interface (API) for
the Perl Language. The DBI API Specification defines a set of
functions, variables and conventions that provide a consistent
database interface independent of the actual database being used.


%prep
%setup -q -n DBI-%{version} 

iconv -f iso8859-1 -t utf-8 lib/DBD/Gofer.pm >lib/DBD/Gofer.pm.new &&
  mv lib/DBD/Gofer.pm{.new,}

chmod 644 ex/*
chmod 744 dbixs_rev.pl

# Filter unwanted Requires:
cat << EOF > %{name}-req
#!/bin/sh
%{__perl_requires} $* |\
  sed -e '/perl(RPC::/d'
EOF

%define __perl_requires %{_builddir}/DBI-%{version}/%{name}-req
chmod +x %{__perl_requires}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

# Remove Win32 specific files and man pages to avoid unwanted dependencies
rm -rf $RPM_BUILD_ROOT%{perl_vendorarch}/{Win32,DBI/W32ODBC.pm} \
	 $RPM_BUILD_ROOT%{_mandir}/man3/{DBI::W32,Win32::DBI}ODBC.3pm

perl -pi -e 's"#!perl -w"#!/usr/bin/perl -w"' \
	$RPM_BUILD_ROOT%{perl_vendorarch}/{goferperf,dbixs_rev}.pl


%check
make test

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README ex/
%{_bindir}/dbipro*
%{_bindir}/dbilogstrip
%{perl_vendorarch}/*.p*
%{perl_vendorarch}/Bundle/
%{perl_vendorarch}/DBD/
%{perl_vendorarch}/DBI/
%{perl_vendorarch}/auto/DBI/
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*


%changelog
* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.609-4
- rebuild against perl 5.10.1

* Thu Sep 24 2009 Stepan Kasal <skasal@redhat.com> - 1.609-3
- provide versioned perl(DBI)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.609-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 10 2009 Stepan Kasal <skasal@redhat.com> - 1.609-1
- new upstream version
- drop unneeded build patch
- move the iconv to convert the source

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.607-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jul 28 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.607-1
- update

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.601-4
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.601-3
- Autorebuild for GCC 4.3

* Tue Jan 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.601-2
- rebuild for new perl

* Fri Oct 26 2007 Robin Norwood <rnorwood@redhat.com> - 1.601-1
- Update to latest CPAN version: 1.601
- Fix some issues from package review:
  - patch to change #! line in script
  - make script executable
  - fix requires and buildrequires

* Mon Aug 27 2007 Robin Norwood <rnorwood@redhat.com> - 1.58-2
- Rebuild

* Mon Aug 13 2007 Robin Norwood <rnorwood@redhat.com> - 1.58-1
- Update to latest CPAN version: 1.58

* Thu Jun 07 2007 Robin Norwood <rnorwood@redhat.com> - 1.56-1
- Update to latest CPAN version: 1.56
- Move the filter requires step into %%prep
- Remove very old patch (for perl 5.8.1)
- Fix a couple of rpmlint issues (non-UTF8 manpage and script with
  incorrect shebang line

* Sat Dec 02 2006 Robin Norwood <rnorwood@redhat.com> - 1.53-1
- Upgrade to latest CPAN version: 1.53

* Thu Aug 24 2006 Robin Norwood <rnorwood@redhat.com> - 1.52-1
- Upgrade to 1.52 for bug #202310
        
* Mon Jul 17 2006 Jason Vas Dias <jvdias@redhat.com> - 1.51-1
- Upgrade to 1.51

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.50-3
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.50-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.50-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 1.50-2
- rebuild for new perl-5.8.8 / gcc / glibc

* Mon Dec 19 2005 Jason Vas Dias<jvdias@redhat.com> - 1.50-1
- upgrade to 1.50

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Wed Apr 13 2005 Jose Pedro Oliveira <jpo@di.uminho.pt> - 1.48-4
- (#154762)
- License information: GPL or Artistic
- Removed the Time::HiRes building requirement (see Changes)
- Removed the empty .bs file
- Corrected file permissions

* Mon Apr 04 2005 Warren Togami <wtogami@redhat.com> 1.48-3
- filter perl(Apache) (#153673)

* Fri Apr 01 2005 Robert Scheck <redhat@linuxnetz.de> 1.48-2
- spec file cleanup (#153164)

* Thu Mar 31 2005 Warren Togami <wtogami@redhat.com> 1.48-1
- 1.48

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 1.40-1
- update to 1.40

* Fri Dec 19 2003 Chip Turner <cturner@redhat.com> 1.39-1
- update to 1.39

* Mon Jul  7 2003 Chip Turner <cturner@redhat.com> 1.37-1
- upgrade to 1.37

* Wed Apr  2 2003 Chip Turner <cturner@redhat.com> 1.32-6
- add buildrequires on perl-Time-HiRes

* Tue Feb 18 2003 Chip Turner <cturner@redhat.com>
- update dependency filter to remove dependency on perl(Apache) that
- crept in (#82927)

* Mon Jan 27 2003 Chip Turner <cturner@redhat.com>
- version bump and rebuild

* Sat Dec 14 2002 Chip Turner <cturner@redhat.com>
- don't use rpm internal dep generator

* Wed Nov 20 2002 Chip Turner <cturner@redhat.com>
- rebuild

* Wed Aug  7 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.30-1
- 1.30. 

* Tue Jun 25 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.28-1
- 1.28
- Building it also fixes #66304

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun  5 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.23-2
- Tweak dependency finder - filter out a dependency found within the 
  doc section of a module

* Tue Jun  4 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.23-1
- 1.23
- Some changes to integrate with new Perl
- Update URL

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May  7 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.21-2
- Rebuild

* Fri Feb 22 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.21-1
- 1.21

* Fri Feb  8 2002 Chip Turner <cturner@redhat.com>
- filter out "soft" dependencies: perl(RPC::PlClient) and perl(Win32::ODBC)

* Thu Feb  7 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.201-2
- Rebuild

* Tue Jan 22 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.201-1
- 1.201

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jan  8 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.20-1
- 1.20
- Proper URL

* Sat Jun 23 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 1.18

* Wed May 30 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 1.16
- change group to Applications/Databases from Applications/CPAN

* Tue May  1 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 1.15

* Tue Feb 27 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Cleanups

* Thu Nov 30 2000 Trond Eivind Glomsrød <teg@redhat.com>
- build for main distribution
- use %%{_tmppath}
- change name of specfile
- don't use a find script to generate file lists
- general cleanup
- add descriptive summary and description

* Mon Aug 14 2000 Tim Powers <timp@redhat.com>
- Spec file was autogenerated. 
