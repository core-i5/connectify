#!/bin/bash

# Make entrypoint scripts executable
chmod +x user_service/entrypoint.sh
chmod +x post_service/entrypoint.sh

# Make dependencies.sh executable
chmod +x dependencies.sh

# Make setup.sh executable
chmod +x setup.sh

# Make remove.sh executable
chmod +x remove.sh

# Run dependencies.sh
./dependencies.sh
