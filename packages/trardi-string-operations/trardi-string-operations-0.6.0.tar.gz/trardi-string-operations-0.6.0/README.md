# String properties and transformations

The purpose of this plugin is return string properties and some transformations as upper case, etc.

# Configuration

This node requires configuration. 

You have to provide a path to string that needs to be transformed. 

```json
{
  "string": "event@path.to.data"
}
```

# Input payload

This node does not process input payload.

# Output

This plugin returns anobject with transformed string and all its properties such as: isdigit, isupper, etc.

## Available properties and transformations

* capitalize - Converts the first character to upper case
* casefold - Converts string into lower case
* isalnum - Returns True if all characters in the string are alphanumeric
* isalpha - Returns True if all characters in the string are in the alphabet 
* isascii - Returns True if all characters in the string are ascii characters
* isdecimal - Returns True if all characters in the string are decimals
* isdigit - Returns True if all characters in the string are digits
* isidentifier - Returns True if the string is an identifier
* islower - Returns True if all characters in the string are lower case
* isnumeric - Returns True if all characters in the string are numeric
* isprintable - Returns True if all characters in the string are printable
* isspace - Returns True if all characters in the string are whitespaces
* istitle - Returns True if the string follows the rules of a title
* isupper - Returns True if all characters in the string are upper case
* lstrip - Returns a left trim version of the string
* swapcase - Swaps cases, lower case becomes upper case and vice ver sa
* title - Converts the first character of each word to upper case
* upper - Converts a string into upper case
* lower - Converts a string into lower case