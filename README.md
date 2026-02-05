# EntraRecon

Yet an other tool to perform the external recon of a tenant.

* What's new? Nothing
* Why? To learn

`Invoke-AADIntReconAsOutsider in python`

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

------------------------------------------------------------
Domain                      | Type      | STS
------------------------------------------------------------    
domain.com                  | Managed   |           
test.domain.com             | Federated | adfs.domain.com                
domain.mail.onmicrosoft.com | Managed   |           
domain.onmicrosoft.com      | Managed   |           
------------------------------------------------------------

Enumerating potential Azure services
Email: domain.mail.protection.outlook.com
SharePoint: domain.sharepoint.com

```
