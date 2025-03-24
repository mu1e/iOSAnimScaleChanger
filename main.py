import traceback
from pathlib import Path
import click
from packaging.version import parse as parse_version
from pymobiledevice3.cli.cli_common import Command
from pymobiledevice3.exceptions import NoDeviceConnectedError, PyMobileDevice3Exception
from pymobiledevice3.lockdown import LockdownClient, create_using_usbmux
from pymobiledevice3.services.installation_proxy import InstallationProxyService
from sparserestore import backup, perform_restore
import shutil
import plistlib

global lockdown
lockdown = create_using_usbmux(autopair=True)

def exit(code=0):
    return code

def apply_animation_speed(service_provider: LockdownClient) -> None:
    if Path('./modded-animation-speed.plist').exists() == False:
        print("Edit your animation speed settings first!")
        return
    device_class = service_provider.get_value(key="DeviceClass")
    device_build = service_provider.get_value(key="BuildVersion")
    device_version = parse_version(service_provider.product_version)

    if not all([device_class, device_build, device_version]):
        click.secho("Failed to get device information!", fg="red")
        click.secho("Make sure your device is connected and try again.", fg="red")
        return
    
    try:
        with open('./modded-animation-speed.plist', "rb") as helper_contents:
            click.secho(f"Replacing /var/Managed Preferences/mobile/com.apple.UIKit.plist", fg="yellow")
            back = backup.Backup(
                files=[
                    backup.ConcreteFile(
                        "",
                        "SysContainerDomain-../../../../../../../../var/Managed Preferences/mobile/com.apple.UIKit.plist",
                        owner=501,
                        group=501,
                        contents=helper_contents.read(),
                    ),
                    backup.ConcreteFile("", "SysContainerDomain-../../../../../../../.." + "/crash_on_purpose", contents=b""),
                ]
            )
    except Exception as e:
        click.secho(f"ERROR: {e}", fg="red")
        return
    try:
        perform_restore(back, reboot=False)
    except PyMobileDevice3Exception as e:
        if "Find My" in str(e):
            click.secho("Find My must be disabled in order to use this tool.", fg="red")
            click.secho("Disable Find My from Settings (Settings -> [Your Name] -> Find My) and then try again.", fg="red")
            exit(1)
        elif "crash_on_purpose" not in str(e):
            raise e

    click.secho("Done! Reboot device and feel free to turn on FindMy", fg="green")

def menu():
    print("\033[1;32mAnimation Speed Modifier\033[0;m")
    print("")
    print("I AM NOT RESPONSIBLE FOR ANYTHING THAT HAPPENS TO YOUR DEVICE")
    print("Back up your device first!")
    exited = False
    while exited is False:
        print("1. Modify animation speed")
        print("2. Apply modified animation speed settings")
        print("3. Exit")
        try:
            option = int(input("Enter option: "))
        except ValueError:
            print("Type in a number!")
            menu()
        if option == 1:
            create_modded_animation_speed()
        elif option == 2:
            apply_animation_speed(lockdown)
        elif option == 3:
            exited = True
            exit(0)

def create_modded_animation_speed():
    if Path('./modded-animation-speed.plist').exists() == False:
        print("Creating duplicate to edit...")
        shutil.copyfile('./original-animation-speed.plist', './modded-animation-speed.plist')
    with open('modded-animation-speed.plist', 'rb') as plistbytes:
        plist = plistlib.loads(plistbytes.read())
        print(f"Current settings: {plist}")
        speed_value = float(input("Enter the desired animation speed (1.0 = default | 0.5 = faster | 2.0 = slower etc.): "))
        plist['UIAnimationDragCoefficient'] = speed_value
        with open('modded-animation-speed.plist', 'wb') as plistbytes:
            plistlib.dump(plist, plistbytes)
            print("Edited plist! Apply it in the previous menu.")

def main():
    try:
        menu()
    except NoDeviceConnectedError:
        click.secho("No device connected!", fg="red")
        click.secho("Please connect your device and try again.", fg="red")
        exit(1)
    except click.UsageError as e:
        click.secho(e.format_message(), fg="red")
        exit(2)
    except Exception:
        click.secho("An error occurred!", fg="red")
        click.secho(traceback.format_exc(), fg="red")
        exit(1)

if __name__ == "__main__":
    main()
