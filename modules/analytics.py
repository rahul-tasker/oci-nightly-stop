# THIS IS AN EXAMPLE SCRIPT - This is not intended for production purposes
# Oracle and it's employees can not be held liable for any unintended consequences of this program
import oci

resource_name = 'analytics instances'

def start_analytics_instances(config, signer, compartments):
    target_resources = []

    print("Listing all {}... (* is marked for start)".format(resource_name))
    for compartment in compartments:
        # print("  compartment: {}".format(compartment.name))
        analytics_instances = _get_resource_list(config, signer, compartment.id)
        for analytics_instance in analytics_instances:
            go = 0
            instance = _get_analytics_instance(config, signer, analytics_instance.id)
            if (instance.lifecycle_state == 'INACTIVE'):
                if ('control' in instance.defined_tags) and ('nightly_stop' in instance.defined_tags['control']): 
                    if (instance.defined_tags['control']['nightly_stop'].upper() != 'FALSE'):
                        go = 1
                else:
                    go = 1

            print("      {} ({}) in {}".format(analytics_instance.name, analytics_instance.lifecycle_state, compartment.name))
            if (go == 1):
                for inst in analytics_instances:
                    if (inst.lifecycle_state == 'INACTIVE'):
                        print("        * analytics instance:{} ({})".format(inst.name, inst.lifecycle_state))
                        target_resources.append(inst)
                    else:
                        print("          analytics instance:{} ({})".format(inst.name, inst.lifecycle_state))

    print('\nStarting * marked {}...'.format(resource_name))
    for resource in target_resources:
        try:
            response = _analytics_start_action(config, signer, resource.id, 'START')
        except oci.exceptions.ServiceError as e:
            print("---------> error. status: {}".format(e))
            pass
        else:
            print("    start requested: {} ({})".format(response.hostname, response.lifecycle_state))
            

    print("\nAll {} started!".format(resource_name))

def stop_analytics_instances(config, signer, compartments):
    target_resources = []

    print("Listing all {}... (* is marked for stop)".format(resource_name))
    for compartment in compartments:
        # print("  compartment: {}".format(compartment.name))
        analytics_instances = _get_resource_list(config, signer, compartment.id)
        for analytics_instance in analytics_instances:
            go = 0
            instance = _get_analytics_instance(config, signer, analytics_instance.id)
            if (instance.lifecycle_state == 'ACTIVE'):
                if ('control' in instance.defined_tags) and ('nightly_stop' in instance.defined_tags['control']): 
                    if (instance.defined_tags['control']['nightly_stop'].upper() != 'FALSE'):
                        go = 1
                else:
                    go = 1

            print("      {} ({}) in {}".format(analytics_instance.name, analytics_instance.lifecycle_state, compartment.name))
            if (go == 1):
                for inst in analytics_instances:
                    if (instance.lifecycle_state == 'ACTIVE'):
                        print("        * analytics instance:{} ({})".format(inst.name, inst.lifecycle_state))
                        target_resources.append(instance)
                    else:
                        print("          analytics instance:{} ({})".format(inst.name, inst.lifecycle_state))

    print('\nStopping * marked {}...'.format(resource_name))
    for resource in target_resources:
        try:
            response = _analytics_stop_action(config, signer, resource.id, 'STOP')
        except oci.exceptions.ServiceError as e:
            print("---------> error. status: {}".format(e))
            pass
        else:
            print("    stop requested: {} ({})".format(response.hostname, response.lifecycle_state))
            
    print("\nAll {} stopped!".format(resource_name))


def _get_resource_list(config, signer, compartment_id):
    object = oci.analytics.AnalyticsClient(config=config, signer=signer)
    resources = oci.pagination.list_call_get_all_results(
        object.list_analytics_instances,
        compartment_id=compartment_id
    )
    return resources.data

def _get_analytics_instance(config, signer, analytics_id):
    object = oci.analytics.AnalyticsClient(config=config, signer=signer)
    instance = object.get_analytics_instance(analytics_instance_id=analytics_id)
    return instance.data



def _get_analytics_list(config, signer, compartment_id, instance_id):
    object = oci.analytics.AnalyticsClient(config=config, signer=signer)
    resources = oci.pagination.list_call_get_all_results(
        object.list_analytics_instances,
        compartment_id = compartment_id,
        instance_id = instance_id
    )
    return resources.data

def _analytics_start_action(config, signer, resource_id, action):
    object = oci.analytics.AnalyticsClient(config=config, signer=signer)
    response = object.start_analytics_instance(
        resource_id
    )
    return response.data

def _analytics_stop_action(config, signer, resource_id, action):
    object = oci.analytics.AnalyticsClient(config=config, signer=signer)
    response = object.stop_analytics_instance(
        resource_id
    )
    return response.data
