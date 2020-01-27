# Provisionar máquinas de Azure con Vagrant

## Instalar CLI de Azure

Prerrequisitos:

```bash
    sudo apt-get install apt-transport-https lsb-release software-properties-common dirmngr -y
```

Añadir a la lista de fuentes:

```bash
    AZ_REPO=$(lsb_release -cs)
    echo "deb [arch=amd64] https://packages.microsoft.com/repos/azure-cli/ $AZ_REPO main" | \
        sudo tee /etc/apt/sources.list.d/azure-cli.list
```

Obtener key de Microsoft:

```bash
    sudo apt-key --keyring /etc/apt/trusted.gpg.d/Microsoft.gpg adv \
       --keyserver packages.microsoft.com \
       --recv-keys BC528686B50D79E339D3721CEB3E94ADBE1229CF
```

Instalar el CLI de Azure:

```bash
    sudo apt-get update
    sudo apt-get install azure-cli
```

## Crear máquina virtual en Azure con Vagrant

Instalar plugin de azure para vagrant:

```bash
    vagrant plugin install vagrant-azure
```

Hacer login con la cuenta de Azure:

```bash
    az login
```

Generar AAD (Azure Active Directory) para poder acceder a nuestros recursos en Azure:

```bash
    az ad sp create-for-rbac
```

De estos dos ultimos comandos hay que exportar como variable de entorno:

```bash
    export AZURE_TENANT_ID=<tenant>
    export AZURE_CLIENT_ID=<appId>
    export AZURE_CLIENT_SECRET=<password>
    export AZURE_SUBSCRIPTION_ID=<id>
```

```vagrantfile

```

He seleccionado una imagen de Ubuntu Server 18.04. Se puede ver las
imagenes existentes con:

```bash
    az vm image list --output table
```

Para ver las regiones existentes para ver cual conviene más:

```bash
    az account list-locations -o table
```

Por ejemplo, se puede ver que existe francesouth. Al estar más cerca escogeré esa.

Para mirar el tipo de máquinas que puedo desplegar en esa región tengo que realizar el
siguiente comando desde el CLI de Azure.

```bash
    az vm list-skus --location francesouth --output table
```

También se ha creado un grupo de recursos desde el Vagrantfile para que estén organizados todos los recuros
en el mismo grupo. Así será mas fácil de administrar.

## Referencias

[Instalar CLI Azure](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-apt?view=azure-cli-latest)  
[Ver Imagenes](https://docs.microsoft.com/en-us/azure/virtual-machines/linux/cli-ps-findimage)  
[Tipos de máquinas](https://docs.microsoft.com/es-es/azure/azure-resource-manager/templates/error-sku-not-available)  
