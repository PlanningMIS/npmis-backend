from django.dispatch import Signal

signal_perform_upgrade = Signal(use_caching=True)
signal_post_initial_setup = Signal(use_caching=True)
signal_post_upgrade = Signal(use_caching=True)
signal_pre_initial_setup = Signal(use_caching=True)
signal_pre_upgrade = Signal(use_caching=True)
signal_npmis_pre_save = Signal(use_caching=True)