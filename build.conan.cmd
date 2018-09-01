set PackageName=Log4qt/1.5.0@common/stable

conan create . %PackageName% -pr msvcprofile
conan create . %PackageName% -pr msvcprofiled

conan upload %PackageName% --all -r=p1


