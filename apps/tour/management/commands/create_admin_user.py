"""
Django management command to create an admin user interactively
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from django.db import IntegrityError
from utils.enums import GroupName
import re


class Command(BaseCommand):
    help = 'Create an admin user with interactive prompts and add to admin group'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n🔐 Admin User Creation Wizard\n'))
        self.stdout.write('=' * 50)

        # Get username
        while True:
            username = self.get_input('Enter username: ')
            if not username:
                self.stdout.write(self.style.WARNING('Username cannot be empty!'))
                continue
            if len(username) < 3:
                self.stdout.write(self.style.WARNING('Username must be at least 3 characters!'))
                continue
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f'Username "{username}" already exists!'))
                continue
            break

        # Get email
        while True:
            email = self.get_input('Enter email: ')
            if not email:
                self.stdout.write(self.style.WARNING('Email cannot be empty!'))
                continue
            if not self.is_valid_email(email):
                self.stdout.write(self.style.WARNING('Invalid email format!'))
                continue
            if User.objects.filter(email=email).exists():
                self.stdout.write(self.style.WARNING(f'Email "{email}" already exists!'))
                continue
            break

        # Get password
        while True:
            password = self.get_input('Enter password (minimum 6 characters): ', hide_input=True)
            if not password:
                self.stdout.write(self.style.WARNING('Password cannot be empty!'))
                continue
            if len(password) < 6:
                self.stdout.write(self.style.WARNING('Password must be at least 6 characters!'))
                continue
            password_confirm = self.get_input('Confirm password: ', hide_input=True)
            if password != password_confirm:
                self.stdout.write(self.style.WARNING('Passwords do not match!'))
                continue
            break

        # Create user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=True,
                is_superuser=False,  # Set to False, will add to admin group
            )
            self.stdout.write(self.style.SUCCESS(f'✓ User "{username}" created successfully!'))
        except IntegrityError as e:
            raise CommandError(f'Error creating user: {e}')

        # Add to admin group
        try:
            admin_group, created = Group.objects.get_or_create(name=GroupName.ADMIN.value)
            if created:
                self.stdout.write(self.style.WARNING('✓ Admin group created'))
            user.groups.add(admin_group)
            self.stdout.write(self.style.SUCCESS(f'✓ User added to "{GroupName.ADMIN.value}" group'))
        except Exception as e:
            raise CommandError(f'Error adding user to admin group: {e}')

        # Summary
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS('✓ Admin user setup complete!\n'))
        self.stdout.write(f'Username: {self.style.WARNING(username)}')
        self.stdout.write(f'Email: {self.style.WARNING(email)}')
        self.stdout.write(f'Group: {self.style.WARNING(GroupName.ADMIN.value)}')
        self.stdout.write('\nYou can now login at /backdoor/\n')

    def get_input(self, prompt, hide_input=False):
        """
        Get user input from command line
        
        Args:
            prompt: The prompt message
            hide_input: If True, hides the input (for passwords)
        """
        if hide_input:
            import getpass
            return getpass.getpass(prompt=prompt)
        else:
            return input(prompt).strip()

    @staticmethod
    def is_valid_email(email):
        """
        Validate email format
        
        Args:
            email: Email address to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
