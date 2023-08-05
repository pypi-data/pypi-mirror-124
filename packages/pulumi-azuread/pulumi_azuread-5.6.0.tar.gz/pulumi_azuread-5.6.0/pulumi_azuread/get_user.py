# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'GetUserResult',
    'AwaitableGetUserResult',
    'get_user',
    'get_user_output',
]

@pulumi.output_type
class GetUserResult:
    """
    A collection of values returned by getUser.
    """
    def __init__(__self__, account_enabled=None, age_group=None, business_phones=None, city=None, company_name=None, consent_provided_for_minor=None, cost_center=None, country=None, creation_type=None, department=None, display_name=None, division=None, employee_id=None, employee_type=None, external_user_state=None, fax_number=None, given_name=None, id=None, im_addresses=None, job_title=None, mail=None, mail_nickname=None, manager_id=None, mobile_phone=None, object_id=None, office_location=None, onpremises_distinguished_name=None, onpremises_domain_name=None, onpremises_immutable_id=None, onpremises_sam_account_name=None, onpremises_security_identifier=None, onpremises_sync_enabled=None, onpremises_user_principal_name=None, other_mails=None, postal_code=None, preferred_language=None, proxy_addresses=None, show_in_address_list=None, state=None, street_address=None, surname=None, usage_location=None, user_principal_name=None, user_type=None):
        if account_enabled and not isinstance(account_enabled, bool):
            raise TypeError("Expected argument 'account_enabled' to be a bool")
        pulumi.set(__self__, "account_enabled", account_enabled)
        if age_group and not isinstance(age_group, str):
            raise TypeError("Expected argument 'age_group' to be a str")
        pulumi.set(__self__, "age_group", age_group)
        if business_phones and not isinstance(business_phones, list):
            raise TypeError("Expected argument 'business_phones' to be a list")
        pulumi.set(__self__, "business_phones", business_phones)
        if city and not isinstance(city, str):
            raise TypeError("Expected argument 'city' to be a str")
        pulumi.set(__self__, "city", city)
        if company_name and not isinstance(company_name, str):
            raise TypeError("Expected argument 'company_name' to be a str")
        pulumi.set(__self__, "company_name", company_name)
        if consent_provided_for_minor and not isinstance(consent_provided_for_minor, str):
            raise TypeError("Expected argument 'consent_provided_for_minor' to be a str")
        pulumi.set(__self__, "consent_provided_for_minor", consent_provided_for_minor)
        if cost_center and not isinstance(cost_center, str):
            raise TypeError("Expected argument 'cost_center' to be a str")
        pulumi.set(__self__, "cost_center", cost_center)
        if country and not isinstance(country, str):
            raise TypeError("Expected argument 'country' to be a str")
        pulumi.set(__self__, "country", country)
        if creation_type and not isinstance(creation_type, str):
            raise TypeError("Expected argument 'creation_type' to be a str")
        pulumi.set(__self__, "creation_type", creation_type)
        if department and not isinstance(department, str):
            raise TypeError("Expected argument 'department' to be a str")
        pulumi.set(__self__, "department", department)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if division and not isinstance(division, str):
            raise TypeError("Expected argument 'division' to be a str")
        pulumi.set(__self__, "division", division)
        if employee_id and not isinstance(employee_id, str):
            raise TypeError("Expected argument 'employee_id' to be a str")
        pulumi.set(__self__, "employee_id", employee_id)
        if employee_type and not isinstance(employee_type, str):
            raise TypeError("Expected argument 'employee_type' to be a str")
        pulumi.set(__self__, "employee_type", employee_type)
        if external_user_state and not isinstance(external_user_state, str):
            raise TypeError("Expected argument 'external_user_state' to be a str")
        pulumi.set(__self__, "external_user_state", external_user_state)
        if fax_number and not isinstance(fax_number, str):
            raise TypeError("Expected argument 'fax_number' to be a str")
        pulumi.set(__self__, "fax_number", fax_number)
        if given_name and not isinstance(given_name, str):
            raise TypeError("Expected argument 'given_name' to be a str")
        pulumi.set(__self__, "given_name", given_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if im_addresses and not isinstance(im_addresses, list):
            raise TypeError("Expected argument 'im_addresses' to be a list")
        pulumi.set(__self__, "im_addresses", im_addresses)
        if job_title and not isinstance(job_title, str):
            raise TypeError("Expected argument 'job_title' to be a str")
        pulumi.set(__self__, "job_title", job_title)
        if mail and not isinstance(mail, str):
            raise TypeError("Expected argument 'mail' to be a str")
        pulumi.set(__self__, "mail", mail)
        if mail_nickname and not isinstance(mail_nickname, str):
            raise TypeError("Expected argument 'mail_nickname' to be a str")
        pulumi.set(__self__, "mail_nickname", mail_nickname)
        if manager_id and not isinstance(manager_id, str):
            raise TypeError("Expected argument 'manager_id' to be a str")
        pulumi.set(__self__, "manager_id", manager_id)
        if mobile_phone and not isinstance(mobile_phone, str):
            raise TypeError("Expected argument 'mobile_phone' to be a str")
        pulumi.set(__self__, "mobile_phone", mobile_phone)
        if object_id and not isinstance(object_id, str):
            raise TypeError("Expected argument 'object_id' to be a str")
        pulumi.set(__self__, "object_id", object_id)
        if office_location and not isinstance(office_location, str):
            raise TypeError("Expected argument 'office_location' to be a str")
        pulumi.set(__self__, "office_location", office_location)
        if onpremises_distinguished_name and not isinstance(onpremises_distinguished_name, str):
            raise TypeError("Expected argument 'onpremises_distinguished_name' to be a str")
        pulumi.set(__self__, "onpremises_distinguished_name", onpremises_distinguished_name)
        if onpremises_domain_name and not isinstance(onpremises_domain_name, str):
            raise TypeError("Expected argument 'onpremises_domain_name' to be a str")
        pulumi.set(__self__, "onpremises_domain_name", onpremises_domain_name)
        if onpremises_immutable_id and not isinstance(onpremises_immutable_id, str):
            raise TypeError("Expected argument 'onpremises_immutable_id' to be a str")
        pulumi.set(__self__, "onpremises_immutable_id", onpremises_immutable_id)
        if onpremises_sam_account_name and not isinstance(onpremises_sam_account_name, str):
            raise TypeError("Expected argument 'onpremises_sam_account_name' to be a str")
        pulumi.set(__self__, "onpremises_sam_account_name", onpremises_sam_account_name)
        if onpremises_security_identifier and not isinstance(onpremises_security_identifier, str):
            raise TypeError("Expected argument 'onpremises_security_identifier' to be a str")
        pulumi.set(__self__, "onpremises_security_identifier", onpremises_security_identifier)
        if onpremises_sync_enabled and not isinstance(onpremises_sync_enabled, bool):
            raise TypeError("Expected argument 'onpremises_sync_enabled' to be a bool")
        pulumi.set(__self__, "onpremises_sync_enabled", onpremises_sync_enabled)
        if onpremises_user_principal_name and not isinstance(onpremises_user_principal_name, str):
            raise TypeError("Expected argument 'onpremises_user_principal_name' to be a str")
        pulumi.set(__self__, "onpremises_user_principal_name", onpremises_user_principal_name)
        if other_mails and not isinstance(other_mails, list):
            raise TypeError("Expected argument 'other_mails' to be a list")
        pulumi.set(__self__, "other_mails", other_mails)
        if postal_code and not isinstance(postal_code, str):
            raise TypeError("Expected argument 'postal_code' to be a str")
        pulumi.set(__self__, "postal_code", postal_code)
        if preferred_language and not isinstance(preferred_language, str):
            raise TypeError("Expected argument 'preferred_language' to be a str")
        pulumi.set(__self__, "preferred_language", preferred_language)
        if proxy_addresses and not isinstance(proxy_addresses, list):
            raise TypeError("Expected argument 'proxy_addresses' to be a list")
        pulumi.set(__self__, "proxy_addresses", proxy_addresses)
        if show_in_address_list and not isinstance(show_in_address_list, bool):
            raise TypeError("Expected argument 'show_in_address_list' to be a bool")
        pulumi.set(__self__, "show_in_address_list", show_in_address_list)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if street_address and not isinstance(street_address, str):
            raise TypeError("Expected argument 'street_address' to be a str")
        pulumi.set(__self__, "street_address", street_address)
        if surname and not isinstance(surname, str):
            raise TypeError("Expected argument 'surname' to be a str")
        pulumi.set(__self__, "surname", surname)
        if usage_location and not isinstance(usage_location, str):
            raise TypeError("Expected argument 'usage_location' to be a str")
        pulumi.set(__self__, "usage_location", usage_location)
        if user_principal_name and not isinstance(user_principal_name, str):
            raise TypeError("Expected argument 'user_principal_name' to be a str")
        pulumi.set(__self__, "user_principal_name", user_principal_name)
        if user_type and not isinstance(user_type, str):
            raise TypeError("Expected argument 'user_type' to be a str")
        pulumi.set(__self__, "user_type", user_type)

    @property
    @pulumi.getter(name="accountEnabled")
    def account_enabled(self) -> bool:
        """
        Whether or not the account is enabled.
        """
        return pulumi.get(self, "account_enabled")

    @property
    @pulumi.getter(name="ageGroup")
    def age_group(self) -> str:
        """
        The age group of the user. Supported values are `Adult`, `NotAdult` and `Minor`.
        """
        return pulumi.get(self, "age_group")

    @property
    @pulumi.getter(name="businessPhones")
    def business_phones(self) -> Sequence[str]:
        """
        A list of telephone numbers for the user.
        """
        return pulumi.get(self, "business_phones")

    @property
    @pulumi.getter
    def city(self) -> str:
        """
        The city in which the user is located.
        """
        return pulumi.get(self, "city")

    @property
    @pulumi.getter(name="companyName")
    def company_name(self) -> str:
        """
        The company name which the user is associated. This property can be useful for describing the company that an external user comes from.
        """
        return pulumi.get(self, "company_name")

    @property
    @pulumi.getter(name="consentProvidedForMinor")
    def consent_provided_for_minor(self) -> str:
        """
        Whether consent has been obtained for minors. Supported values are `Granted`, `Denied` and `NotRequired`.
        """
        return pulumi.get(self, "consent_provided_for_minor")

    @property
    @pulumi.getter(name="costCenter")
    def cost_center(self) -> str:
        """
        The cost center associated with the user.
        """
        return pulumi.get(self, "cost_center")

    @property
    @pulumi.getter
    def country(self) -> str:
        """
        The country/region in which the user is located, e.g. `US` or `UK`.
        """
        return pulumi.get(self, "country")

    @property
    @pulumi.getter(name="creationType")
    def creation_type(self) -> str:
        """
        Indicates whether the user account was created as a regular school or work account (`null`), an external account (`Invitation`), a local account for an Azure Active Directory B2C tenant (`LocalAccount`) or self-service sign-up using email verification (`EmailVerified`).
        """
        return pulumi.get(self, "creation_type")

    @property
    @pulumi.getter
    def department(self) -> str:
        """
        The name for the department in which the user works.
        """
        return pulumi.get(self, "department")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        The display name of the user.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def division(self) -> str:
        """
        The name of the division in which the user works.
        """
        return pulumi.get(self, "division")

    @property
    @pulumi.getter(name="employeeId")
    def employee_id(self) -> str:
        """
        The employee identifier assigned to the user by the organisation.
        """
        return pulumi.get(self, "employee_id")

    @property
    @pulumi.getter(name="employeeType")
    def employee_type(self) -> str:
        """
        Captures enterprise worker type. For example, Employee, Contractor, Consultant, or Vendor.
        """
        return pulumi.get(self, "employee_type")

    @property
    @pulumi.getter(name="externalUserState")
    def external_user_state(self) -> str:
        """
        For an external user invited to the tenant, this property represents the invited user's invitation status. Possible values are `PendingAcceptance` or `Accepted`.
        """
        return pulumi.get(self, "external_user_state")

    @property
    @pulumi.getter(name="faxNumber")
    def fax_number(self) -> str:
        """
        The fax number of the user.
        """
        return pulumi.get(self, "fax_number")

    @property
    @pulumi.getter(name="givenName")
    def given_name(self) -> str:
        """
        The given name (first name) of the user.
        """
        return pulumi.get(self, "given_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="imAddresses")
    def im_addresses(self) -> Sequence[str]:
        """
        A list of instant message voice over IP (VOIP) session initiation protocol (SIP) addresses for the user.
        """
        return pulumi.get(self, "im_addresses")

    @property
    @pulumi.getter(name="jobTitle")
    def job_title(self) -> str:
        """
        The user’s job title.
        """
        return pulumi.get(self, "job_title")

    @property
    @pulumi.getter
    def mail(self) -> str:
        """
        The SMTP address for the user.
        """
        return pulumi.get(self, "mail")

    @property
    @pulumi.getter(name="mailNickname")
    def mail_nickname(self) -> str:
        """
        The email alias of the user.
        """
        return pulumi.get(self, "mail_nickname")

    @property
    @pulumi.getter(name="managerId")
    def manager_id(self) -> str:
        """
        The object ID of the user's manager.
        """
        return pulumi.get(self, "manager_id")

    @property
    @pulumi.getter(name="mobilePhone")
    def mobile_phone(self) -> str:
        """
        The primary cellular telephone number for the user.
        """
        return pulumi.get(self, "mobile_phone")

    @property
    @pulumi.getter(name="objectId")
    def object_id(self) -> str:
        """
        The object ID of the user.
        """
        return pulumi.get(self, "object_id")

    @property
    @pulumi.getter(name="officeLocation")
    def office_location(self) -> str:
        """
        The office location in the user's place of business.
        """
        return pulumi.get(self, "office_location")

    @property
    @pulumi.getter(name="onpremisesDistinguishedName")
    def onpremises_distinguished_name(self) -> str:
        """
        The on-premises distinguished name (DN) of the user, synchronised from the on-premises directory when Azure AD Connect is used.
        """
        return pulumi.get(self, "onpremises_distinguished_name")

    @property
    @pulumi.getter(name="onpremisesDomainName")
    def onpremises_domain_name(self) -> str:
        """
        The on-premises FQDN, also called dnsDomainName, synchronised from the on-premises directory when Azure AD Connect is used.
        """
        return pulumi.get(self, "onpremises_domain_name")

    @property
    @pulumi.getter(name="onpremisesImmutableId")
    def onpremises_immutable_id(self) -> str:
        """
        The value used to associate an on-premise Active Directory user account with their Azure AD user object.
        """
        return pulumi.get(self, "onpremises_immutable_id")

    @property
    @pulumi.getter(name="onpremisesSamAccountName")
    def onpremises_sam_account_name(self) -> str:
        """
        The on-premise SAM account name of the user.
        """
        return pulumi.get(self, "onpremises_sam_account_name")

    @property
    @pulumi.getter(name="onpremisesSecurityIdentifier")
    def onpremises_security_identifier(self) -> str:
        """
        The on-premises security identifier (SID), synchronised from the on-premises directory when Azure AD Connect is used.
        """
        return pulumi.get(self, "onpremises_security_identifier")

    @property
    @pulumi.getter(name="onpremisesSyncEnabled")
    def onpremises_sync_enabled(self) -> bool:
        """
        Whether this user is synchronised from an on-premises directory (`true`), no longer synchronised (`false`), or has never been synchronised (`null`).
        """
        return pulumi.get(self, "onpremises_sync_enabled")

    @property
    @pulumi.getter(name="onpremisesUserPrincipalName")
    def onpremises_user_principal_name(self) -> str:
        """
        The on-premise user principal name of the user.
        """
        return pulumi.get(self, "onpremises_user_principal_name")

    @property
    @pulumi.getter(name="otherMails")
    def other_mails(self) -> Sequence[str]:
        """
        A list of additional email addresses for the user.
        """
        return pulumi.get(self, "other_mails")

    @property
    @pulumi.getter(name="postalCode")
    def postal_code(self) -> str:
        """
        The postal code for the user's postal address. The postal code is specific to the user's country/region. In the United States of America, this attribute contains the ZIP code.
        """
        return pulumi.get(self, "postal_code")

    @property
    @pulumi.getter(name="preferredLanguage")
    def preferred_language(self) -> str:
        """
        The user's preferred language, in ISO 639-1 notation.
        """
        return pulumi.get(self, "preferred_language")

    @property
    @pulumi.getter(name="proxyAddresses")
    def proxy_addresses(self) -> Sequence[str]:
        """
        List of email addresses for the user that direct to the same mailbox.
        """
        return pulumi.get(self, "proxy_addresses")

    @property
    @pulumi.getter(name="showInAddressList")
    def show_in_address_list(self) -> bool:
        """
        Whether or not the Outlook global address list should include this user.
        """
        return pulumi.get(self, "show_in_address_list")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        The state or province in the user's address.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="streetAddress")
    def street_address(self) -> str:
        """
        The street address of the user's place of business.
        """
        return pulumi.get(self, "street_address")

    @property
    @pulumi.getter
    def surname(self) -> str:
        """
        The user's surname (family name or last name).
        """
        return pulumi.get(self, "surname")

    @property
    @pulumi.getter(name="usageLocation")
    def usage_location(self) -> str:
        """
        The usage location of the user.
        """
        return pulumi.get(self, "usage_location")

    @property
    @pulumi.getter(name="userPrincipalName")
    def user_principal_name(self) -> str:
        """
        The user principal name (UPN) of the user.
        """
        return pulumi.get(self, "user_principal_name")

    @property
    @pulumi.getter(name="userType")
    def user_type(self) -> str:
        """
        The user type in the directory. Possible values are `Guest` or `Member`.
        """
        return pulumi.get(self, "user_type")


class AwaitableGetUserResult(GetUserResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetUserResult(
            account_enabled=self.account_enabled,
            age_group=self.age_group,
            business_phones=self.business_phones,
            city=self.city,
            company_name=self.company_name,
            consent_provided_for_minor=self.consent_provided_for_minor,
            cost_center=self.cost_center,
            country=self.country,
            creation_type=self.creation_type,
            department=self.department,
            display_name=self.display_name,
            division=self.division,
            employee_id=self.employee_id,
            employee_type=self.employee_type,
            external_user_state=self.external_user_state,
            fax_number=self.fax_number,
            given_name=self.given_name,
            id=self.id,
            im_addresses=self.im_addresses,
            job_title=self.job_title,
            mail=self.mail,
            mail_nickname=self.mail_nickname,
            manager_id=self.manager_id,
            mobile_phone=self.mobile_phone,
            object_id=self.object_id,
            office_location=self.office_location,
            onpremises_distinguished_name=self.onpremises_distinguished_name,
            onpremises_domain_name=self.onpremises_domain_name,
            onpremises_immutable_id=self.onpremises_immutable_id,
            onpremises_sam_account_name=self.onpremises_sam_account_name,
            onpremises_security_identifier=self.onpremises_security_identifier,
            onpremises_sync_enabled=self.onpremises_sync_enabled,
            onpremises_user_principal_name=self.onpremises_user_principal_name,
            other_mails=self.other_mails,
            postal_code=self.postal_code,
            preferred_language=self.preferred_language,
            proxy_addresses=self.proxy_addresses,
            show_in_address_list=self.show_in_address_list,
            state=self.state,
            street_address=self.street_address,
            surname=self.surname,
            usage_location=self.usage_location,
            user_principal_name=self.user_principal_name,
            user_type=self.user_type)


def get_user(mail_nickname: Optional[str] = None,
             object_id: Optional[str] = None,
             user_principal_name: Optional[str] = None,
             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetUserResult:
    """
    Gets information about an Azure Active Directory user.

    ## API Permissions

    The following API permissions are required in order to use this data source.

    When authenticated with a service principal, this data source requires one of the following application roles: `User.Read.All` or `Directory.Read.All`

    When authenticated with a user principal, this data source does not require any additional roles.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azuread as azuread

    example = azuread.get_user(user_principal_name="user@hashicorp.com")
    ```


    :param str mail_nickname: The email alias of the user.
    :param str object_id: The object ID of the user.
    :param str user_principal_name: The user principal name (UPN) of the user.
    """
    __args__ = dict()
    __args__['mailNickname'] = mail_nickname
    __args__['objectId'] = object_id
    __args__['userPrincipalName'] = user_principal_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azuread:index/getUser:getUser', __args__, opts=opts, typ=GetUserResult).value

    return AwaitableGetUserResult(
        account_enabled=__ret__.account_enabled,
        age_group=__ret__.age_group,
        business_phones=__ret__.business_phones,
        city=__ret__.city,
        company_name=__ret__.company_name,
        consent_provided_for_minor=__ret__.consent_provided_for_minor,
        cost_center=__ret__.cost_center,
        country=__ret__.country,
        creation_type=__ret__.creation_type,
        department=__ret__.department,
        display_name=__ret__.display_name,
        division=__ret__.division,
        employee_id=__ret__.employee_id,
        employee_type=__ret__.employee_type,
        external_user_state=__ret__.external_user_state,
        fax_number=__ret__.fax_number,
        given_name=__ret__.given_name,
        id=__ret__.id,
        im_addresses=__ret__.im_addresses,
        job_title=__ret__.job_title,
        mail=__ret__.mail,
        mail_nickname=__ret__.mail_nickname,
        manager_id=__ret__.manager_id,
        mobile_phone=__ret__.mobile_phone,
        object_id=__ret__.object_id,
        office_location=__ret__.office_location,
        onpremises_distinguished_name=__ret__.onpremises_distinguished_name,
        onpremises_domain_name=__ret__.onpremises_domain_name,
        onpremises_immutable_id=__ret__.onpremises_immutable_id,
        onpremises_sam_account_name=__ret__.onpremises_sam_account_name,
        onpremises_security_identifier=__ret__.onpremises_security_identifier,
        onpremises_sync_enabled=__ret__.onpremises_sync_enabled,
        onpremises_user_principal_name=__ret__.onpremises_user_principal_name,
        other_mails=__ret__.other_mails,
        postal_code=__ret__.postal_code,
        preferred_language=__ret__.preferred_language,
        proxy_addresses=__ret__.proxy_addresses,
        show_in_address_list=__ret__.show_in_address_list,
        state=__ret__.state,
        street_address=__ret__.street_address,
        surname=__ret__.surname,
        usage_location=__ret__.usage_location,
        user_principal_name=__ret__.user_principal_name,
        user_type=__ret__.user_type)


@_utilities.lift_output_func(get_user)
def get_user_output(mail_nickname: Optional[pulumi.Input[Optional[str]]] = None,
                    object_id: Optional[pulumi.Input[Optional[str]]] = None,
                    user_principal_name: Optional[pulumi.Input[Optional[str]]] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetUserResult]:
    """
    Gets information about an Azure Active Directory user.

    ## API Permissions

    The following API permissions are required in order to use this data source.

    When authenticated with a service principal, this data source requires one of the following application roles: `User.Read.All` or `Directory.Read.All`

    When authenticated with a user principal, this data source does not require any additional roles.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azuread as azuread

    example = azuread.get_user(user_principal_name="user@hashicorp.com")
    ```


    :param str mail_nickname: The email alias of the user.
    :param str object_id: The object ID of the user.
    :param str user_principal_name: The user principal name (UPN) of the user.
    """
    ...
