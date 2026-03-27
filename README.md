# EntraRecon

Yet an other tool to perform the external recon of a tenant.

* What's new? Nothing
* Why? To learn

`Invoke-AADIntReconAsOutsider in python`

**/!\ ACS domains enum has been fixed so this part doesn't work anymore**

Related domains are checked using the api from https://micahvandeusen.com/tools/tenant-domains/
This is based on scrapped domains so expect a lot of domains in the tenant to be missing.

Also note it attempts to get the MOERA (.onmicrosoft.com) domain from DKIM but it might fails. In such cases, you can try to find it manually using using variations on the found domains such as adding sa, group or the tld at the end. (domain.com -> try domaingroup.onmicrosoft.com)



## Installation

```
pipx install git+https://github.com/Mauriceter/EntraRecon.git
```

## Usage

```
entrarecon -d domain.com
```

Example output

```
entrarecon -d domain.com            

General Information
Tenant Brand:     Domain S.A.
Tenant Name:      domain.onmicrosoft.com
Tenant ID:        11111111-1111-1111-1111-11111111
Tenant Region:    EU

OnPrem Information
DesktopSSO:    Enabled
Cloud Sync:    Disabled
MDI Instance:  domain.atp.azure.com
Autodiscover:  autodiscover.domain.com (hosted by microsoft)

----------------------------------------------------------------------------
Domain                      | Type      | STS              | DKIM
----------------------------------------------------------------------------
test.com                    | Managed   |                  | test.onmicrosoft.com
domain.com                  | Managed   |                  | domain.onmicrosoft.com 
test.domain.com             | Federated | adfs.domain.com  | test.onmicrosoft.com          
domain.mail.onmicrosoft.com | Managed   |                  |
domain.onmicrosoft.com      | Managed   |                  | domain.onmicrosoft.com  
----------------------------------------------------------------------------

Enumerating potential Azure services
Email: domain.mail.protection.outlook.com
SharePoint: domain.sharepoint.com

```
