#!/usr/bin/env python3
"""
Script to collect storage disk information from a Cisco IMC server using imcsdk.
"""
from imcsdk.imchandle import ImcHandle
import sys
import csv
from datetime import datetime


def connect_to_cimc(ip_address, username, password):
    """
    Connect to CIMC server.    
    Args:
        ip_address: IP address of the CIMC server
        username: Username for authentication
        password: Password for authentication    
    Returns:
        ImcHandle object if successful, None otherwise
    """
    try:
        handle = ImcHandle(ip_address, username, password)
        handle.login()
        print(f"Successfully connected to CIMC server: {ip_address}")
        return handle
    except Exception as e:
        print(f"Error connecting to CIMC server: {str(e)}")
        return None


def get_physical_disks(handle):
    """
    Get all physical disks information.
    
    Args:
        handle: ImcHandle object
    
    Returns:
        List of physical disk objects
    """
    try:
        # Query all StorageLocalDisk objects
        disks = handle.query_classid("StorageLocalDisk")
        return disks if disks else []
    except Exception as e:
        print(f"Error retrieving physical disks: {str(e)}")
        return []



def format_disk_info(disks, cimc_ip, server_name):
    """
    Format physical disk information for display.
    
    Args:
        disks: List of physical disk objects
        cimc_ip: CIMC IP address to include in the disk info
        server_name: CIMC server name to include in the disk info
    
    Returns:
        List of dictionaries containing disk information
    """
    disk_info = []
    for disk in disks:
        info = {
            'server_name': server_name,
            'cimc_ip': cimc_ip,
            'id': getattr(disk, 'id', 'N/A'),
            'vendor': getattr(disk, 'vendor', 'N/A'),
            'model': getattr(disk, 'product_id', 'N/A'),
            'serial': getattr(disk, 'drive_serial_number', 'N/A'),
            'size': getattr(disk, 'coerced_size', 'N/A'),
            'interface_type': getattr(disk, 'interface_type', 'N/A'),
            'media_type': getattr(disk, 'media_type', 'N/A'),
            'health': getattr(disk, 'drive_state', 'N/A'),
            'firmware': getattr(disk, 'drive_firmware', 'N/A'),
            'pd_status': getattr(disk, 'pd_status', 'N/A'),
        }
        disk_info.append(info)
    return disk_info

def print_storage_info( disks_info):
    """
    Print formatted storage information.
    """
    print("\n" + "="*80)
    
    print("\n" + "="*80)
    print("PHYSICAL DISKS")
    print("="*80)
    if disks_info:
        for idx, disk in enumerate(disks_info, 1):
            print(f"\nDisk {idx}:")
            for key, value in disk.items():
                print(f"  {key.replace('_', ' ').title()}: {value}")
    else:
        print("No physical disks found.")   
    


def save_to_csv(disks_info, filename, write_header=False):
    """
    Save storage information to CSV file.
    
    Args:
        disks_info: List of disk information dictionaries
        filename: Output CSV filename
        write_header: Whether to write the header row (True for first write)
    """
    if not disks_info:
        return
    
    try:
        # Get all unique keys from all disks
        fieldnames = list(disks_info[0].keys())
        
        mode = 'w' if write_header else 'a'
        with open(filename, mode, newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if write_header:
                writer.writeheader()
            writer.writerows(disks_info)
    except Exception as e:
        print(f"Error saving to CSV file: {str(e)}")


def read_cimc_list(input_file):
    """
    Read CIMC server details from CSV file.
    
    Args:
        input_file: Path to the CSV file containing CIMC details
        
    Returns:
        List of dictionaries with server_name, ip, username, password
    """
    cimc_servers = []
    try:
        with open(input_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cimc_servers.append({
                    'server_name': row.get('server_name', '').strip(),
                    'ip': row.get('ip', '').strip(),
                    'username': row.get('username', '').strip(),
                    'password': row.get('password', '').strip()
                })
        return cimc_servers
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        print("Please create a CSV file with columns: server_name,ip,username,password")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading input file: {str(e)}")
        sys.exit(1)


def main():
    """
    Main function to collect and display storage information.
    """
    input_file = "cimcip.csv"
    output_file = "storagediskinfo.csv"
    
    # Read CIMC server list
    print(f"Reading CIMC server list from {input_file}...")
    cimc_servers = read_cimc_list(input_file)
    
    if not cimc_servers:
        print("No CIMC servers found in the input file.")
        sys.exit(1)
    
    print(f"Found {len(cimc_servers)} CIMC server(s) to process.\n")
    
    total_disks = 0
    first_write = True
    
    for idx, server in enumerate(cimc_servers, 1):
        server_name = server['server_name']
        cimc_ip = server['ip']
        cimc_username = server['username']
        cimc_password = server['password']
        
        if not cimc_ip or not cimc_username or not cimc_password:
            print(f"[{idx}/{len(cimc_servers)}] Skipping invalid entry: {server}")
            continue
        
        display_name = f"{server_name} ({cimc_ip})" if server_name else cimc_ip
        print(f"[{idx}/{len(cimc_servers)}] Processing CIMC: {display_name}")
        
        # Connect to CIMC
        handle = connect_to_cimc(cimc_ip, cimc_username, cimc_password)
        
        if not handle:
            print(f"Failed to connect to CIMC server {display_name}. Skipping.\n")
            continue
        
        try:
            # Collect storage information
            physical_disks = get_physical_disks(handle)
            print(f"Found {len(physical_disks)} physical disk(s)")
            
            if physical_disks:
                # Format the information with CIMC IP and server name
                disks_info = format_disk_info(physical_disks, cimc_ip, server_name)
                
                # Display the information
                print_storage_info(disks_info)
                
                # Save to CSV file (append mode after first write)
                save_to_csv(disks_info, output_file, write_header=first_write)
                first_write = False
                total_disks += len(physical_disks)
            else:
                print("No disks found on this server.")
            
        except Exception as e:
            print(f"Error collecting storage information from {cimc_ip}: {str(e)}")
        
        finally:
            # Logout from CIMC
            try:
                handle.logout()
                print(f"Disconnected from CIMC server {cimc_ip}.\n")
            except:
                pass
    
    # Final summary
    print("="*80)
    print(f"Processing complete!")
    print(f"Total CIMC servers processed: {len(cimc_servers)}")
    print(f"Total disks collected: {total_disks}")
    if total_disks > 0:
        print(f"Results saved to: {output_file}")
    print("="*80)


if __name__ == "__main__":
    main()
