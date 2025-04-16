from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("dashboard/", views.IndexView.as_view(), name="index"),
    path("orders/", views.OrderView.as_view(), name="orders"),
    path(
        "order/<str:order_id>/detail/",
        views.OrderDetailView.as_view(),
        name="order_detail",
    ),
    path(
        "invoice/<str:order_id>/",
        views.InvoiceView.as_view(),
        name="invoice",
    ),
    path("order/update/", views.OrderUpdateView.as_view(), name="order_update"),
    # catgory
    path("categories/", views.CategoryListView.as_view(), name="categories"),
    path(
        "category/create/", views.CategoryCreateView.as_view(), name="category_create"
    ),
    path(
        "category/<str:pk>/update/",
        views.CategoryUpdate.as_view(),
        name="category_update",
    ),
    path(
        "category/<str:pk>/delete/",
        views.CategoryDelete.as_view(),
        name="category_delete",
    ),
    # product
    path("products/", views.ProductListView.as_view(), name="product_list"),
    path("product/create/", views.CreateProductView.as_view(), name="product_create"),
    path("product/<pk>/edit/", views.edit_product, name="product_update"),
    path(
        "product/<str:pk>/delete/", views.ProductDelete.as_view(), name="product_delete"
    ),
    # reviews
    path("reviews/", views.ReviewListView.as_view(), name="review_list"),
    path("review/create/", views.ReviewCreateView.as_view(), name="review_create"),
    path("review/<pk>/edit/", views.ReviewUpdateView.as_view(), name="review_update"),
    path(
        "review/<str:pk>/delete/",
        views.ReviewDeleteView.as_view(),
        name="review_delete",
    ),
    # tag
    path("tags/", views.TagListView.as_view(), name="tags"),
    path("tag/create/", views.TagCreateView.as_view(), name="tag_create"),
    path("tag/<str:pk>/update/", views.TagUpdateView.as_view(), name="tag_update"),
    path("tag/<str:pk>/delete/", views.TagDeleteView.as_view(), name="tag_delete"),
    # state
    path("states/", views.StateListView.as_view(), name="states"),
    path("state/create/", views.StateCreateView.as_view(), name="state_create"),
    path(
        "state/<str:pk>/update/", views.StateUpdateView.as_view(), name="state_update"
    ),
    path(
        "state/<str:pk>/delete/", views.StateDeleteView.as_view(), name="state_delete"
    ),
    # district
    path("districts/", views.DistrictListView.as_view(), name="districts"),
    path(
        "district/create/", views.DistrictCreateView.as_view(), name="district_create"
    ),
    path(
        "district/<str:pk>/update/",
        views.DistrictUpdateView.as_view(),
        name="district_update",
    ),
    path(
        "district/<str:pk>/delete/",
        views.DistrictDeleteView.as_view(),
        name="district_delete",
    ),
    # customer
    path("customers/", views.CustomerListView.as_view(), name="customers"),
     # sliders
    path("sliders/", views.SliderListView.as_view(), name="sliders"),

    path(
        "slider/create/", views.SliderCreateView.as_view(), name="slider_create"
    ),
    path(
        "slider/<str:pk>/update/",
        views.SliderUpdateView.as_view(),
        name="slider_update",
    ),
    path(
        "slider/<str:pk>/delete/",
        views.SliderDeleteView.as_view(),
        name="slider_delete",
    ),
    #offer
    path("offers/", views.OfferListView.as_view(), name="offers"),
    path("offer/create/", views.OfferCreateView.as_view(), name="offer_create"),
    path("offer/<str:pk>/update/", views.OfferUpdateView.as_view(), name="offer_update"),
    path("offer/<str:pk>/delete/", views.OfferDeleteView.as_view(), name="offer_delete"),
    
    #Popup Offer
    
    path("popupoffers/", views.PopupOfferListView.as_view(), name="popupoffers"),
    path("popupoffer/create/", views.PopupOfferCreateView.as_view(), name="popupoffer_create"),
    path("popupoffer/<str:pk>/update/", views.PopupOfferUpdateView.as_view(), name="popupoffer_update"),
    path("popupoffer/<str:pk>/delete/", views.PopupOfferDeleteView.as_view(), name="popupoffer_delete"),
    
    # Shipping Fee
    path("shippingfees/", views.ShippingListView.as_view(), name="shippingfees"),
    path("shippingfee/create/", views.ShippingCreateView.as_view(), name="shippingfee_create"),
    path("shippingfee/<str:pk>/update/", views.ShippingUpdateView.as_view(), name="shippingfee_update"),
    path("shippingfee/<str:pk>/delete/", views.ShippingDeleteView.as_view(), name="shippingfee_delete"),
    
    # Contact
    path("contact/", views.ContactListView.as_view(), name="contacts"),
    path("contact/<str:pk>/delete/", views.ContactDeleteView.as_view(), name="contact_delete"),
    path("contact/<str:pk>/update/", views.ContactUpdateView.as_view(), name="contact_update"),
    path("contact/create/", views.ContactCreateView.as_view(), name="contact_create"),
    
    #testimonial
    path("testimonials/", views.TestimonialListView.as_view(), name="testimonials"),
    path("testimonial/create/", views.TestimonialCreateView.as_view(), name="testimonial_create"),
    path("testimonial/<str:pk>/update/", views.TestimonialUpdateView.as_view(), name="testimonial_update"),
    path("testimonial/<str:pk>/delete/", views.TestimonialDeleteView.as_view(), name="testimonial_delete"),
]
