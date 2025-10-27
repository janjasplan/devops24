#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule

def main():
    
    module = AnsibleModule(
        argument_spec=dict(
        message=dict(type='str', required=True)
    ),
        supports_check_mode=True
    )

    message = module.params['message']
    reversed_message = message[::-1]

    # Determine if message differs from its reversed version
    changed = message != reversed_message

    # Handle explicit fail case
    if message == "fail me":
        module.fail_json(
            msg="You requested this to fail",
            changed=True,
            original_message=message,
            reversed_message=reversed_message
        )

    # Return success result
    result = dict(
        changed=changed,
        original_message=message,
        reversed_message=reversed_message
    )

    module.exit_json(**result)


if __name__ == '__main__':
    main()
