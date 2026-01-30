# CIMC Storage Disk Information Collector

A Python script to collect storage disk information from multiple Cisco IMC (Integrated Management Controller) servers and export the data to CSV format.

## Description

This script connects to multiple CIMC servers, retrieves physical disk information from each server, and consolidates all the data into a single CSV file for easy analysis and reporting.

## Features

- Connects to multiple CIMC servers in batch mode
- Collects comprehensive storage disk information including:
  - Disk ID, vendor, model, and serial number
  - Disk size and interface type
  - Media type (SSD/HDD)
  - Health status and firmware version
  - PD (Physical Drive) status
- Exports data to CSV format with server identification
- Progress tracking for multiple server processing
- Error handling for failed connections

## Requirements

- Python 3.6 or higher
- imcsdk library

## Installation

1. Clone or download this repository

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Create a CSV file named `cimcip.csv` in the same directory as the script with the following format:

```csv
server_name,ip,username,password
Server1,192.168.1.100,admin,password123
Server2,192.168.1.101,admin,password123
Server3,192.168.1.102,admin,password123
```

**Columns:**
- `server_name`: Friendly name for the CIMC server
- `ip`: IP address of the CIMC server
- `username`: CIMC login username
- `password`: CIMC login password

## Usage

Run the script:

```bash
python3 collect_storage_info.py
```

The script will:
1. Read all CIMC server details from `cimcip.csv`
2. Connect to each server sequentially
3. Collect storage disk information
4. Display the information on screen
5. Save all results to `storagediskinfo.csv`

## Output

The script generates a file named `storagediskinfo.csv` containing:

| Column | Description |
|--------|-------------|
| server_name | Name of the CIMC server |
| cimc_ip | IP address of the CIMC server |
| id | Disk ID |
| vendor | Disk vendor/manufacturer |
| model | Disk model number |
| serial | Disk serial number |
| size | Disk size |
| interface_type | Interface type (SAS, SATA, etc.) |
| media_type | Media type (SSD, HDD) |
| health | Disk health status |
| firmware | Firmware version |
| pd_status | Physical drive status |

## Example Output

```
Reading CIMC server list from cimcip.csv...
Found 3 CIMC server(s) to process.

[1/3] Processing CIMC: Server1 (192.168.1.100)
Successfully connected to CIMC server: 192.168.1.100
Found 4 physical disk(s)
...
Disconnected from CIMC server 192.168.1.100.

[2/3] Processing CIMC: Server2 (192.168.1.101)
...

================================================================================
Processing complete!
Total CIMC servers processed: 3
Total disks collected: 12
Results saved to: storagediskinfo.csv
================================================================================
```

## Error Handling

- If a server connection fails, the script will skip that server and continue with the next one
- Invalid entries in `cimcip.csv` will be skipped with a warning message
- All errors are logged to the console

## Security Notes

⚠️ **Important**: The `cimcip.csv` file contains sensitive credentials. Ensure proper file permissions and never commit this file to version control.

```bash
# Set restrictive permissions on the credentials file
chmod 600 cimcip.csv
```

## Troubleshooting

**Connection Errors:**
- Verify the CIMC IP address is reachable
- Check username and password are correct
- Ensure the CIMC web interface is accessible

**No Disks Found:**
- Verify the server has physical disks installed
- Check that the storage controller is properly configured

**Import Errors:**
- Ensure imcsdk is installed: `pip install imcsdk`
- Verify Python version is 3.6 or higher

## License

This project is provided as-is for use with Cisco UCS servers.

## Author

Created for CIMC server storage management and monitoring.
# CIMC_LocalDisk_information
