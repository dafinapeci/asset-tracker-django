from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Asset, CheckoutLog, User
from .serializers import AssetSerializer, CheckoutLogSerializer

@api_view(['GET'])
def get_all_assets(request):
# Check if Flutter asked for a specific status (like ?status=AVAILABLE)
    status_filter = request.query_params.get('status')

    if status_filter:
        assets = Asset.objects.filter(status=status_filter)
    else:
        assets = Asset.objects.all()

    serializer = AssetSerializer(assets, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def checkouts(request):
    if request.method == 'GET':
        logs = CheckoutLog.objects.all()
        serializer = CheckoutLogSerializer(logs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        asset_id = request.data.get('assetId')

        # FOOLPROOF FIX: Ignore the Flutter ID and just grab the first User (Dafina)
        user = User.objects.first()
        if not user:
            user = User.objects.create(name="Dafina", role="USER")

        try:
            asset = Asset.objects.get(id=asset_id)
        except Asset.DoesNotExist:
            return Response({'error': f'Asset {asset_id} not found'}, status=status.HTTP_400_BAD_REQUEST)

        if asset.status != 'AVAILABLE':
            return Response({'error': 'Asset unavailable'}, status=status.HTTP_400_BAD_REQUEST)

        asset.status = 'PENDING'
        asset.save()
        CheckoutLog.objects.create(user=user, asset=asset)
        return Response({'status': 'Success'}, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def approve_checkout(request, pk):
    log = get_object_or_404(CheckoutLog, id=pk)
    log.status = 'APPROVED'
    log.save()

    asset = log.asset
    asset.status = 'CHECKED_OUT'
    asset.save()
    return Response({'status': 'Approved'})

@api_view(['PUT'])
def reject_checkout(request, pk):
    log = get_object_or_404(CheckoutLog, id=pk)
    log.status = 'REJECTED'
    log.save()

    asset = log.asset
    asset.status = 'AVAILABLE'
    asset.save()
    return Response({'status': 'Rejected'})

@api_view(['GET'])
def user_checkouts(request, pk):
    user = User.objects.first()
    if not user:
        return Response([])

    logs = CheckoutLog.objects.filter(user=user)
    serializer = CheckoutLogSerializer(logs, many=True)
    return Response(serializer.data)