/**
Logging debugging and error handling
**/
var noConsole = false;

// visual studio has a stupid intellisense for "debugger" which hijacks your attempts to type "debug("
function debug()
{
	log,apply(this, arguments);
}

function log()
{
	try
	{
		if( checkConsole() )
	    {
			if( console['firebug'] !== undefined && console['firebug'] !== null )
			{
				console.log.apply(this,arguments);
			} else
			{
				// for( var x = 0; x < arguments.length; x++ )
				// {
					// console.log(arguments[x]);
				// }
			}
	    }
	} catch(ex)
	{
		noConsole = true;
	}
}

function logError(msg)
{
    debug(msg);
}

function group()
{
	if( checkConsole() ) 
	{
		if( console['firebug'] !== undefined && console['firebug'] !== null )
		{
			console.group.apply(this, arguments);
		} else
		{
			log.apply(this, arguments);
		}
	}
}

function groupEnd()
{
	if( checkConsole() ) console.groupEnd();
}

function checkConsole()
{
	try
	{
		if( !noConsole && console !== undefined && console !== null )
		{
			noConsole = false;
		} else
		{
			noConsole = true;
		}
	} catch(ex)
	{
		noConsole = true;
	}
	
	return !noConsole;
}