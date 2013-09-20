
# Please replace the URL and the URL in Source0
# with correct project URLs
# and of course others
Name:           MyDocs-docs
Version:        1
Release:        1
Summary:        Documentation and Samples for a project
License:        LGPLv2+
URL:            http://www.MyDocs.org
Source0:        http://MyDocs.org/%{name}-%{version}-%{release}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Group:          Documentation
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  python-docutils
BuildRequires:  python-sphinx

%description
My docs packaged as an RPM

%prep
%setup -q -n %{name}-%{version}-%{release}

%build
make html

%install
mkdir -p %{buildroot}/%{_defaultdocdir}
cp -r %{_builddir}/%{name}-%{version}-%{release}/_build/html %{buildroot}/%{_defaultdocdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_defaultdocdir}/%{name}
