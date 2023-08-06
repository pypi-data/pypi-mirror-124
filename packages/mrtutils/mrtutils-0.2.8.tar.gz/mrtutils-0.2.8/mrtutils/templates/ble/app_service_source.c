/**
 * @file app_${obj.prefix}_svc.c
 * @brief Application layer for ${obj.name} service
 * @date ${obj.profile.genTime}
 * 
 */

/*user-block-includes-start -------------------------------------------------*/
#include "svc/${obj.prefix}_svc.h"

/* Private Variables ---------------------------------------------------------*/   
% for char in obj.chars:
 %if hasattr(char, 'default'):
    %if char.type == 'string':
    ${ "char* {0}_{1}_default = \"{2}\";".format(obj.prefix,char.name.lower(), char.default) }
    %else:
        %if  (char.arrayLen > 1):
    ${ "{0}_{1}_t {0}_{1}_default[] = {2};".format(obj.prefix,char.name.lower(), char.default) }
        %else:
            %if char.isEnum and type(char.default) == str :
    ${ "{0}_{1}_t {0}_{1}_default = {2}_{3}_{4};".format(obj.prefix,char.name.lower(),obj.prefix.upper(), char.name.upper(), char.default.upper() )}
            %else: 
    ${ "{0}_{1}_t {0}_{1}_default = {2};".format(obj.prefix,char.name.lower(), char.default) }
            %endif
        %endif
    %endif
%endif
%endfor


/*user-block-includes-end*/



/* Post Init -----------------------------------------------------------------*/

/**
 * @brief Called after GATT Server is intialized
 */
void ${obj.prefix}_svc_post_init_handler(void)
{
% for char in obj.chars:
    %if hasattr(char, 'default'):
        %if char.type == 'string':
    ${ "{0}_set_{1}({0}_{1}_default);".format(obj.prefix,char.name.lower()) }
        %else:
            %if  (char.arrayLen > 1):
    ${ "{0}_set_{1}({0}_{1}_default, sizeof({0}_{1}_default));".format(obj.prefix,char.name.lower() )}
            %else:
    ${ "{0}_set_{1}({0}_{1}_default);".format(obj.prefix,char.name.lower() )}
            %endif
        %endif
    %endif
%endfor
    //TODO initialize characteristic values 
}

/* Characteristic Event Handlers----------------------------------------------*/

% for char in obj.chars:
/**
 * @brief Handles GATT event on ${char.name} Characteristic
 * @param event - ptr to mrt_gatt_evt_t event with data and event type
 */
${"mrt_status_t {0}_{1}_handler(mrt_gatt_evt_t* event)".format(obj.prefix,char.name.lower())}
{

%if (char.arrayLen > 1):
%if (char.type == 'string'):
    //char* val = (char*) event->data.value); /* Cast to correct data type*/
%else:
    //${"{0}_{1}_t* vals = ({0}_{1}_t*) event->data.value;".format(obj.prefix,char.name.lower())}  /* Cast to correct data type*/
    //${"uint32_t len = event.data.len/sizof({0}_{1}_t);".format(obj.prefix,char.name.lower())}   /* Get length of array*/
%endif
%else:
    //${"{0}_{1}_t val = *(({0}_{1}_t*) event->data.value);".format(obj.prefix,char.name.lower())} /* Cast to correct data type*/
%endif


% if char.isEnum> 0:
    //switch(val)
    //{
    % for val in char.vals:
    //    case ${t.padAfter(obj.prefix +"_"+char.name + "_"+val.name+":" , 45).upper()}  /* ${val.desc} */
    //        //TODO Handle ${val.name}
    //        break;
    % endfor 
    //    default: 
    //        break;
    //}

%endif
% if char.isMask> 0:
    % for val in char.vals:
    //if(val & ${t.padAfter(obj.prefix +"_"+char.name + "_"+val.name+")" , 45).upper()}  /* ${val.desc} */
    //{
    //  //TODO Handle ${val.name} 
    //}
    % endfor

%endif
    //TODO Handle ${char.name} Characteristic events
    return MRT_STATUS_OK;
}

% endfor
