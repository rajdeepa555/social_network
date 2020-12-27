from core.routers import router as post_router

router_urlpatterns = []

# including user app api's
router_urlpatterns += post_router.urls
