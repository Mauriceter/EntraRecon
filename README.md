# entrarecon

Yet an other tool to perform the external recon of a tenant.

* What's new? Nothing
* Why? To learn

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

Tenant Brand:     Domain S.A.
Tenant Name:      domain.onmicrosoft.com
Tenant ID:        6fbe6025-1d0f-498d-ae44-23b34f048283
Tenant Region:    EU

DesktopSSO:       Enabled
MDI Instance:     domain.atp.azure.com
Autodiscover:     autodiscover.domain.com (hosted by microsoft)

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
