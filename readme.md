# Development Guide

## Optional: Development Containers (Docker + VSCode)
This project includes an **optional Dev Container** configuration to make Python development reproducible and isolated, without requiring developers to install specific Python versions or dependencies on their host machine.

> **Important:** Using the Dev Container is completely optional.  
> You can continue to use a locally installed Python environment if you prefer.

---

### What is a Dev Container?

A Dev Container is a Docker-based development environment that VS Code can attach to.  
When enabled, VS Code runs your workspace **inside a container** that has:

- A pinned Python version
- All required dependencies
- A consistent Linux environment

This helps avoid issues like:
- “Works on my machine”
- Conflicting Python versions
- Dependency drift between developers or customers

## DevContainer Setup When Using WSL2 & Instrument Communication

When running the devcontainer inside WSL2 on Windows, Docker requires network mirroring and direct NIC passthrough to communicate with instruments connected via Ethernet.

### Prerequisites
1. **Configure WSL2 Mirrored Networking**
   Create or edit the `.wslconfig` file in your Windows user profile folder  (`%USERPROFILE%\.wslconfig`) aka (`C:\Users\<YourUsername>\.wslconfig`):

   ```ini
   [wsl2]
   networkingMode=mirrored
   ```

2. **Restart WSL**
   ```PowerShell
   wsl --shutdown
   ```

3. **Create the Pass-through Docker Network**
Identify the name of the Network Interface Card (NIC) connected to your instrument (e.g. "Ethernet 4" via ipconfig or Get-NetAdapter). Run the following commaind in Windows PowerShell:

    ```PowerShell
    docker network create -d transparent -o com.docker.network.windowsshim.interface="Ethernet 4" host_ethernet_net
    ```

Now you can launch the project using VS Codes Reopen in Container prompt.