from ariadne import load_schema_from_path
from ariadne.objects import ObjectType
from cryptofolio.resolvers import user_account

user_account_type_defs = load_schema_from_path(
    'cryptofolio/schema/user_account')

user_account_mutation = ObjectType("Mutation")

user_account_mutation.set_field('signUp',
                                user_account.sign_up_resolver)
user_account_mutation.set_field('activateAccount',
                                user_account.activate_account_resolver)
user_account_mutation.set_field('generateActivationCode',
                                user_account.generate_activation_code_resolver)
user_account_mutation.set_field('signIn',
                                user_account.sign_in_resolver)
user_account_mutation.set_field('accountStatus',
                                user_account.account_status_resolver)
user_account_mutation.set_field('addExchange',
                                user_account.add_exchange_resolver)
user_account_mutation.set_field('generatePswdRecoveryCode',
                                user_account.generate_pswd_recovery_code_resolver)
user_account_mutation.set_field('recoverPassword',
                                user_account.recover_password_resolver)
user_account_mutation.set_field('deleteAccount',
                                user_account.delete_account_resolver)        
user_account_mutation.set_field('changePassword',
                                user_account.change_password_resolver)
user_account_mutation.set_field('deleteExchange',
                                user_account.delete_exchange_resolver)

