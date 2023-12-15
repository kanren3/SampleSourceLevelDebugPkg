#include <Uefi.h>

#include <Library/UefiLib.h>
#include <Library/DebugLib.h>
#include <Library/DevicePathLib.h>
#include <Library/UefiBootServicesTableLib.h>
#include <Library/UefiRuntimeServicesTableLib.h>

#include <Protocol/LoadedImage.h>

#include "WaitDebugger.h"

EFI_STATUS
EFIAPI
LoadSampleSourceLevelDebugDxe(
    IN EFI_HANDLE ImageHandle
)
{
    EFI_STATUS Status;
    EFI_LOADED_IMAGE_PROTOCOL *LoadedImage;
    EFI_DEVICE_PATH_PROTOCOL *DevicePath;
    EFI_HANDLE DxeImageHandle;

    Status = gBS->HandleProtocol(ImageHandle, &gEfiLoadedImageProtocolGuid, &LoadedImage);

    if (EFI_SUCCESS != Status) {
        return Status;
    }

    DevicePath = FileDevicePath(LoadedImage->DeviceHandle, L"\\SampleSourceLevelDebugDxe.efi");

    if (NULL == DevicePath) {
        return EFI_NOT_FOUND;
    }

    Status = gBS->LoadImage(FALSE, ImageHandle, DevicePath, NULL, 0, &DxeImageHandle);

    if (EFI_SUCCESS != Status) {
        return Status;
    }

    Status = gBS->StartImage(DxeImageHandle, NULL, NULL);

    if (EFI_SUCCESS != Status) {
        return Status;
    }

    return EFI_SUCCESS;
}

EFI_STATUS
EFIAPI
UefiUnload(
    IN EFI_HANDLE ImageHandle
)
{
    return EFI_SUCCESS;
}

EFI_STATUS
EFIAPI
UefiMain(
    IN EFI_HANDLE ImageHandle,
    IN EFI_SYSTEM_TABLE *SystemTable
)
{
    EFI_STATUS Status;

    WaitDebugger();

    Status = LoadSampleSourceLevelDebugDxe(ImageHandle);

    return Status;
}