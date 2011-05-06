def feed_created(sender, **kwargs):
   if not kwargs.get('created', False): return

   inst = kwargs.get('instance', None)
   if inst: inst.update()
