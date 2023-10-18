# Rename all "ai_development" from blueprint to a target project name, e.g. "h2ki_service".

# Global variable
TARGET_STRING="h2ki_service"

# Function to recursively rename files and directories
rename_recursive() {
  shopt -s dotglob # Include hidden files
  for file in "$1"/*; do
    new_file="${file//ai_development/$TARGET_STRING}"
    if [ "$file" != "$new_file" ]; then
      mv "$file" "$new_file"
      file="$new_file"
    fi
    if [ -d "$file" ]; then
      rename_recursive "$file"
    else
      mime_type=$(file --mime-type -b "$file")
      if [[ $mime_type == text/* || "${file##*.}" == "json" ]]; then
        sed -i "s/ai_development/$TARGET_STRING/g" "$file"
      fi
    fi
  done
  shopt -u dotglob # Revert to default (exclude hidden files)
}

# Call function with root directory
rename_recursive .
