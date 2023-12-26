# Rename all "ai-development" from blueprint to TARGET_STRING_HYPHEN.
# Rename all "ai_development" from blueprint to TARGET_STRING_UNDERSCORE.

# Global variables
TARGET_STRING_HYPHEN="my-project"
TARGET_STRING_UNDERSCORE="my_project"

# Function to recursively rename files and directories
rename_recursive() {
  shopt -s dotglob # Include hidden files
  for file in "$1"/*; do
    new_file="${file//ai-development/$TARGET_STRING_HYPHEN}"
    new_file="${new_file//ai_development/$TARGET_STRING_UNDERSCORE}"
    if [ "$file" != "$new_file" ]; then
      mv "$file" "$new_file"
      file="$new_file"
    fi
    if [ -d "$file" ]; then
      rename_recursive "$file"
    else
      mime_type=$(file --mime-type -b "$file")
      if [[ $mime_type == text/* || "${file##*.}" == "json" ]]; then
        sed -i "s/ai-development/$TARGET_STRING_HYPHEN/g" "$file"
        sed -i "s/ai_development/$TARGET_STRING_UNDERSCORE/g" "$file"
      fi
    fi
  done
  shopt -u dotglob # Revert to default (exclude hidden files)
}

# Call function with root directory
rename_recursive .
