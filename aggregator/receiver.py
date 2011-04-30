try: from settings import UPDATE_ON_FEED_CREATION
except ImportError: from aggregator.aggregator_settings import UPDATE_ON_FEED_CREATION

def feed_created(sender, **kwargs):
   if not kwargs.get('created', False) or not UPDATE_ON_FEED_CREATION: return

   inst = kwargs.get('instance', None)
   if inst: inst.update()
