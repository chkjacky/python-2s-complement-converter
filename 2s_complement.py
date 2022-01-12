from itertools import product
import re
import math

# REPLACE / INVERT NUMBERS
def multiwordReplace( text, wordDic ):
    rc = re.compile( '|'.join( map( re.escape, wordDic ) ) )
    def translate(match):
        return wordDic[match.group(0)]
    return rc.sub( translate, text )

# ADD NUMBER TO BINARY
def add_binary( x, y ):
    result = ''
    carry = 0
    maxlen = max( len(x), len(y) )

    # Normalize lengths
    x = x.zfill( maxlen )
    y = y.zfill( maxlen )

    for i in range( maxlen-1, -1, -1 ):
        r = carry
        r += 1 if x[i] == '1' else 0
        r += 1 if y[i] == '1' else 0

        # r can be 0,1,2,3 (carry + x[i] + y[i])
        # and among these, for r==1 and r==3 you will have result bit = 1
        # for r==2 and r==3 you will have carry = 1

        result = ('1' if r % 2 == 1 else '0') + result
        carry = 0 if r < 2 else 1    

    if carry != 0 : result = '1' + result

    return result.zfill( maxlen )  

# DIVIDE DENARY BY 2 REPEATEDLY
def divide_denary_by_2( denary ):
    binary = ""
    bitLen = 8
    
    print("\nSteps of conversion: ")
    print("\nThe whole / integral part of the denary: ")
    
    if( denary > 0 ):
        print("\n2 |__", str( denary ) )
    else:
        print("\n2 |__", str( denary ), "-> 0" )
    
    while denary > 0:
        # Concatenate bits
        binary =  str( denary % 2 ) + binary

        # Get the remainder after divided the denary by 2
        remainder = str( denary % 2 )
        
        # Floor division and rounds the result down to the nearest whole number
        denary = denary // 2

        print("2 |__", str( denary ), "->", remainder ) 
    
    # Check whether the size of the binary is 8
    if( len( str( binary ) ) < 8 ):
        # Determine how much we should add at the beginning of the binary
        bitLen = bitLen - ( len( str( binary ) ) )

        for c in range( bitLen ):
            binary = "0" + binary

            if( len( str ( binary ) ) == 8 ):
                break

    return binary

# CONVERT DECIMAL/DENARY TO BINARY
def convert_denary_to_binary( denary ):
    # Declare and assign value to variables
    binary      = ""
    remainder   = ""
    dec_int     = ""
    dec_frac    = ""
    bin_frac    = ""
    one         = "1"
    zero        = "0"
    answer      = "\n\nTherefore, the 2's binary in signed 8-bit is:\t"
    isNegative  = False

    # Dictionary will be used to invert the binary numbers
    inverseBin = {
        "0": "1",
        "1": "0"
    }

    print("\n..::Converting" , denary , "to binary ::..")

    if( denary == 0 ):
        print("The decimal number", denary, "in binary is 0.")
        return False

    # Check whether the denary is a negative value
    if( denary >= 0 ):
        isNegative = False
    elif( denary < 0 ):
        isNegative = True

    # Absolute the denary to get rid of the negative sign
    denary = abs( denary )

    if( type( denary ) == int ):
        # Divide denary by 2 repeatedly
        binary = divide_denary_by_2( denary )

        # Check whether we need to do 2's complement or not based on the value of the denary
        if( isNegative ):
            # Invert the binary numbers
            binary = multiwordReplace( binary, inverseBin )

            print("\n1's Complement - Invert the binary number:\t", binary )

            # Fill zeros and concatenate a plus sign
            one = "+ " + one.zfill( 8 )

            # Add 1 to the inverted binary for 2's complement
            newBin = add_binary( binary, "1" )

            # Display columnar addition
            print( "\n2's Complement - Add 1 to the binary number:" )
            print( " ", binary )
            print( one, "\n-----------")
            print( " ", newBin, "\n===========" )

            print( answer, newBin )

        else:
            print( answer, binary )
    
    elif( type( denary ) == float ):
        sDec = "{0:.8f}".format( float( denary ) )                                # Convert the denary from float to string   
        dec_int = int( str( sDec ).split( "." ) [0] )                             # Get the whole/integral part of the denary number using . as delimiter
        dec_frac = float("{0:.8f}".format( float( sDec ) - float( dec_int ) ) )  # Get the fractional part of the denary number

        # Divide denary by 2 repeatedly
        binary = divide_denary_by_2( dec_int )

        print("\n\nThe fractional part of the denary: \n")
        for i in range(8):
            print("{0:.8f}".format( dec_frac, 2 ), "* 2 =", "{0:.8f}".format( dec_frac * 2, 2 ), " | ", math.floor( dec_frac * 2 ) )
            
            # Multiple the fractional part by 2 repeatedly
            dec_frac = dec_frac * 2

            # Concatenate the bit in a string
            bin_frac = bin_frac + str( int( dec_frac ) )

            # Subtract 1 from the product if it is more than 1
            if( dec_frac >= 1 ):
                dec_frac = dec_frac - 1

        # Check whether we need to do 2's complement or not based on the value of the denary
        if( isNegative ):
            # Invert the binary numbers of the whole/integral part of the denary
            binary = multiwordReplace( binary, inverseBin )

            print("\n1's Complement - Invert the whole/integral part of th denary:\t", binary )

            # Invert the binary numbers of the fractional part of the denary
            bin_frac = multiwordReplace( bin_frac, inverseBin )

            print("\n1's Complement - Invert the fractional part of th denary:\t", bin_frac )

            # Display the combination of both integral part and fractional part together
            print("\nCombine both integral part and fractional part:\t\t\t", ( binary + "." + bin_frac ) )

            # Add 1 to the inverted binary that combined the integral and fractional part (2's complement)
            # Note that we do not have a decimal point here
            newBin = add_binary( ( binary + bin_frac ), "1" )

            # Get the length of the integral part binary
            binaryLen = len( binary )

            #Separate the integral part and fractional part by adding a decimal point
            newBin = newBin[:binaryLen] + "." + newBin[binaryLen:]

            # Display columnar addition
            print( "\n2's Complement - Add 0." + one.zfill( len( bin_frac ) ) + " to the binary number:" )
            print( " ", ( binary + "." + bin_frac ) )
            print( "+ " + zero.zfill(len( binary ) ) + "." + one.zfill( len( bin_frac ) ), "\n--------------------")
            print( " ", newBin, "\n====================" )

            print( answer, newBin )

        else:
            print( answer, binary + "." + bin_frac )


# FUNCTION CALLING
x = 0

# # Whole number
# convert_denary_to_binary( 0 )
# convert_denary_to_binary( -101 )
# convert_denary_to_binary( 100 )

# # Floating number
# convert_denary_to_binary( -101.703125 )
# convert_denary_to_binary( -98.5625 )
# convert_denary_to_binary( -55.75 )
# convert_denary_to_binary( -0.0625 )
# convert_denary_to_binary( 27.5 )
# convert_denary_to_binary( 98.5625 )
# convert_denary_to_binary( -127.5625 )

while( x != -1 ):
    userInput = input("\nInput a decimal number:\t")

    # Check whether the userInput is an integer or a float using regular expression
    if( re.match("[-+]?\d+$", userInput) ):
        # Convert the userInput to integer
    	userInput = int( userInput )
    elif( re.match("[+-]?((\.\d+)|(\d+(\.\d+)?))$", userInput) ):
        # Convert the userInput to float
    	userInput = float( userInput )
    else:
        # Display error message and restart the while loop
    	print("Invalid Input! Please enter an integer or a float. \n")
    	continue

    if( userInput >= 128 or userInput <= -128 ):
    	print("Out of range! Enter decimal number less than 128 and more than -128. \n")
    else:
    	convert_denary_to_binary( userInput )