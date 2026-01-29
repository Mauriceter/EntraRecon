import argparse
import requests
import re
import sys
import socket


def bold(text):
    return f"\033[1m{str(text)}\033[0m"

class EntraRecon:
    def __init__(self, domain):
        self.domain = domain
        self.domains = None
        self.tenantbrand = None
        self.tenantname = None
        self.tenantid = None
        self.tenantregion = None
        self.allazureservices = { # from https://github.com/NetSPI/MicroBurst/blob/1990ea38d13876cc282c5863a2ff4bcfc88a20c0/Misc/Invoke-EnumerateAzureSubDomains.ps1#L77
            "onmicrosoft.com": "Microsoft Hosted Domain",
            "scm.azurewebsites.net": "App Services - Management",
            "azurewebsites.net": "App Services",
            "p.azurewebsites.net": "App Services",
            "cloudapp.net": "App Services",
            "file.core.windows.net": "Storage Accounts - Files",
            "blob.core.windows.net": "Storage Accounts - Blobs",
            "queue.core.windows.net": "Storage Accounts - Queues",
            "table.core.windows.net": "Storage Accounts - Tables",
            "mail.protection.outlook.com": "Email",
            "sharepoint.com": "SharePoint",
            "redis.cache.windows.net": "Databases - Redis",
            "documents.azure.com": "Databases - Cosmos DB",
            "database.windows.net": "Databases - MSSQL",
            "vault.azure.net": "Key Vaults",
            "azureedge.net": "CDN",
            "search.windows.net": "Search Appliance",
            "azure-api.net": "API Services",
            "azurecr.io": "Azure Container Registry",
            "eastus.cloudapp.azure.com": "East US Virtual Machines",
            "eastus2.cloudapp.azure.com": "East US 2 Virtual Machines",
            "westus.cloudapp.azure.com": "West US Virtual Machines",
            "westus2.cloudapp.azure.com": "West US 2 Virtual Machines",
            "westus3.cloudapp.azure.com": "West US 3 Virtual Machines",
            "centralus.cloudapp.azure.com": "Central US Virtual Machines",
            "northcentralus.cloudapp.azure.com": "North Central US Virtual Machines",
            "southcentralus.cloudapp.azure.com": "South Central US Virtual Machines",
            "westcentralus.cloudapp.azure.com": "West Central US Virtual Machines",
            "northeurope.cloudapp.azure.com": "North Europe (Ireland) Virtual Machines",
            "westeurope.cloudapp.azure.com": "West Europe (Netherlands) Virtual Machines",
            "uksouth.cloudapp.azure.com": "United Kingdom South Virtual Machines",
            "ukwest.cloudapp.azure.com": "United Kingdom West Virtual Machines",
            "francecentral.cloudapp.azure.com": "France Central Virtual Machines",
            "germanywestcentral.cloudapp.azure.com": "Germany West Central Virtual Machines",
            "italynorth.cloudapp.azure.com": "Italy North Virtual Machines",
            "norwayeast.cloudapp.azure.com": "Norway East Virtual Machines",
            "polandcentral.cloudapp.azure.com": "Poland Central Virtual Machines",
            "spaincentral.cloudapp.azure.com": "Spain Central Virtual Machines",
            "swedencentral.cloudapp.azure.com": "Sweden Central Virtual Machines",
            "switzerlandnorth.cloudapp.azure.com": "Switzerland North Virtual Machines",
            "australiaeast.cloudapp.azure.com": "Australia East Virtual Machines",
            "australiacentral.cloudapp.azure.com": "Australia Central Virtual Machines",
            "australiasoutheast.cloudapp.azure.com": "Australia Southeast Virtual Machines",
            "centralindia.cloudapp.azure.com": "Central India Virtual Machines",
            "southindia.cloudapp.azure.com": "South India Virtual Machines",
            "japaneast.cloudapp.azure.com": "Japan East Virtual Machines",
            "japanwest.cloudapp.azure.com": "Japan West Virtual Machines",
            "koreacentral.cloudapp.azure.com": "Korea Central Virtual Machines",
            "koreasouth.cloudapp.azure.com": "Korea South Virtual Machines",
            "eastasia.cloudapp.azure.com": "East Asia (Hong Kong) Virtual Machines",
            "southeastasia.cloudapp.azure.com": "Southeast Asia (Singapore) Virtual Machines",
            "newzealandnorth.cloudapp.azure.com": "New Zealand North Virtual Machines",
            "canadacentral.cloudapp.azure.com": "Canada Central Virtual Machines",
            "canadaeast.cloudapp.azure.com": "Canada East Virtual Machines",
            "uaenorth.cloudapp.azure.com": "UAE North Virtual Machines",
            "qatarcentral.cloudapp.azure.com": "Qatar Central Virtual Machines",
            "israelcentral.cloudapp.azure.com": "Israel Central Virtual Machines",
            "southafricanorth.cloudapp.azure.com": "South Africa North Virtual Machines",
            "mexicocentral.cloudapp.azure.com": "Mexico Central Virtual Machines",
            "brazilsouth.cloudapp.azure.com": "Brazil South Virtual Machines",
        }
        self.azureservices = []

    def check_tenant(self):
        url = f"https://login.microsoftonline.com/{self.domain}/.well-known/openid-configuration"
        response = requests.get(url, timeout=10)
        try:
            response.raise_for_status()
        except:
            print(f"No tenant associated with {self.domain}")
            sys.exit(0)

        data = response.json()
        self.tenantregion = data.get('tenant_region_scope')
        self.tenantid = data.get('issuer')[24:-1]

        self.check_federated(self.domain, True)

    def check_federated(self, domain, detail=False):
        url = f"https://login.microsoftonline.com/GetUserRealm.srf?login=aaaa@{domain}"

        response = requests.get(url, timeout=10)
        data = response.json()
        sts = ""
        dtype = data.get('NameSpaceType')
        if dtype == "Federated":
            sts = data.get('AuthURL').split("/")[2]
        
        if detail:
            self.tenantbrand = data.get('FederationBrandName')
        
        return (dtype, sts)

    def get_tenant_domains_from_acs(self):

        url = f"https://accounts.accesscontrol.windows.net/{self.domain}/metadata/json/1"

        response = requests.get(url, timeout=10)
        data = response.json()

        domains = set()
        audiences = data.get("allowedAudiences", [])

        for audience in audiences:
            match = re.search(r"@(.+)$", audience)
            if match:
                domain = match.group(1)

                # Filter out GUID-only entries (tenant IDs)
                if not re.fullmatch(
                    r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
                    domain,
                    re.IGNORECASE,
                ):
                    domains.add(domain)

        self.domains = sorted(domains)

    def check_destopsso(self):
        body = {
            "username": f"test@{self.domain}",
            "isOtherIdpSupported": True,
            "checkPhones": True,
            "isRemoteNGCSupported": True,
            "isCookieBannerShown": False,
            "isFidoSupported": True,
            "originalRequest": "",
            "flowToken": "",
        }
        url = "https://login.microsoftonline.com/common/GetCredentialType"
        headers = {
            "User-Agent": "hello",
            "Content-Type": "application/json; charset=UTF-8",
        }
        response = requests.post(url, json=body, headers=headers)
        userRealm = response.json()
        
        desktop_sso = userRealm["EstsProperties"].get("DesktopSsoEnabled", False)
        return desktop_sso
    
    def check_mdi(self):
        tenant = self.tenantname.split(".", 1)[0]

        domains = [
            f"{tenant}.atp.azure.com",
            f"{tenant}-onmicrosoft-com.atp.azure.com",
        ]

        for domain in domains:
            try:
                socket.gethostbyname(domain)
                return domain
            except socket.gaierror:
                continue
        return "No"
    
    # https://www.netspi.com/blog/technical-blog/cloud-pentesting/enumerating-azure-services/
    def check_azureservices(self):
        keywords = [self.tenantname.split(".", 1)[0]]  # add keywork variations later

        for service in self.allazureservices:
            for keyword in keywords:
                try:
                    socket.gethostbyname(f"{keyword}.{service}")
                    self.azureservices.append((f"{keyword}.{service}",self.allazureservices[service]))
                except socket.gaierror:
                    continue

    def check_autodiscover(self):
        host = f"autodiscover.{self.domain}"
        try:
            hostname, aliases, ips = socket.gethostbyname_ex(host)
            microsoft_suffixes = (
                ".outlook.com",
                ".office365.com",
                ".office.com",
                ".protection.outlook.com"
            )

            hosting = "self-hosted"
            for name in [hostname] + aliases:
                if name.endswith(microsoft_suffixes):
                    hosting = "hosted by microsoft"
                    break

            return f"autodiscover.{self.domain} ({hosting})"
        except socket.gaierror:
            return "Not found"



def main():
    parser = argparse.ArgumentParser(
        description="Entra ID external recon"
    )

    parser.add_argument("-d", "--domain", required=True, help="Domain to analyze")
    args = parser.parse_args()

    entrarecon = EntraRecon(args.domain)
    
    entrarecon.check_tenant()
    entrarecon.get_tenant_domains_from_acs()

    max_len = max(len(d) for d in entrarecon.domains)
    entrarecon.tenantname = next((d for d in entrarecon.domains if d.endswith(".onmicrosoft.com") and not d.endswith(".mail.onmicrosoft.com")),"")
    

    print('')
    print(f"{bold('Tenant Brand:'):25} {entrarecon.tenantbrand}")
    print(f"{bold('Tenant Name:'):25} {entrarecon.tenantname}")
    print(f"{bold('Tenant ID:'):25} {entrarecon.tenantid}")
    print(f"{bold('Tenant Region:'):25} {entrarecon.tenantregion}")
    print('')
    print(f"{bold('DesktopSSO:'):25} {"Enabled" if entrarecon.check_destopsso() else "Disabled"}")
    print(f"{bold('MDI Instance:'):25} {entrarecon.check_mdi()}")
    print(f"{bold('Autodiscover:'):25} {entrarecon.check_autodiscover()}")
    print('')
    print("-" * (max_len+25))
    print(f"{bold('Domain'):{max_len+8}} | {bold('Type'):17} | {bold('STS'):10}")
    print("-" * (max_len+25))
    for domain in entrarecon.domains:
        (dtype, sts) = entrarecon.check_federated(domain)
        print(f"{domain:{max_len}} | {dtype:9} | {sts:10}")
    print("-" * (max_len+25))
    print('')

    entrarecon.check_azureservices()

    print(bold('Enumerating potential Azure services'))
    for service in entrarecon.azureservices:
        print(f"{bold(service[1])}: {service[0]}")


if __name__ == "__main__":
    main()