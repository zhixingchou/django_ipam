from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.template import loader

from .models import SuperBlock
from .models import Subnet

from .forms import NewSuperNet
from .forms import NewSubNet

import netaddr


def index(request):
    supernets_list = SuperBlock.objects.all()
    subnets_list = Subnet.objects.all()
    template = loader.get_template('ipam/index.html')
    context = RequestContext(request, {
        'supernets_list': supernets_list,
        'subnets_list': subnets_list,
    })
    return HttpResponse(template.render(context))


def view_supernet(request, supernet_id):
    supernet = SuperBlock.objects.get(id=supernet_id)
    return render(request, 'ipam/supernet.html', {'supernet': supernet}) 


def new_supernet(request):
    if request.method == 'POST':
        form = NewSuperNet(request.POST)
        region = form['region']
        if form.is_valid():
            address_space = form.cleaned_data['address_space']
            region = form.cleaned_data['region']
            try:
                if netaddr.IPNetwork(address_space):
                    new = SuperBlock(address_space = address_space,
                                     region = region,)
                    new.save() 
                    messages.success(request, "{0} was sucessfully added."
                                     .format(address_space))
            except:
                messages.error(request, "Error adding {0}."
                               .format(address_space))
                return HttpResponseRedirect('/ipam/supernet/new/')
            return HttpResponseRedirect('/ipam/')
        else:
            messages.error(request, "Invalid request.")
            return HttpResponseRedirect('/ipam/supernet/new/')
    else:
        form = NewSuperNet()
        return render(request, 'ipam/new_supernet.html',
                      {'form': form})


def edit_supernet(request, supernet_id):
    if request.method == 'GET':
        try:
            supernet = SuperBlock.objects.get(id=supernet_id)
            return render(request, 'ipam/edit_supernet.html',
                          {'supernet': supernet})
        except:
            messages.error(request, "Error. Unknown supernet")
            return HttpResponseRedirect('/ipam/')
    else:
        form = NewSuperNet(request.POST)
        region = form['region']
        if form.is_valid():
            address_space = form.cleaned_data['address_space']
            region = form.cleaned_data['region']
            try:
                if netaddr.IPNetwork(address_space):
                    SuperBlock.objects.filter(id=supernet_id).\
                        update(address_space = address_space,
                                      region = region,)
                    messages.success(request, "Updated {0} successfully."
                                     .format(address_space))
                    return HttpResponseRedirect('/ipam/')
            except:
                messages.error(request, "Error updating {0}. Invalid Syntax."
                               .format(address_space))
                return HttpResponseRedirect('/ipam/supernet/edit/{0}'
                                            .format(supernet_id))
        else:
            messages.error(request, "Invalid request.")
            return HttpResponseRedirect('/ipam/supernet/edit/{0}'
                                        .format(supernet_id))


def delete_supernet(request, supernet_id):
    try:
        supernet = SuperBlock.objects.get(id=supernet_id)
        SuperBlock.objects.filter(address_space=supernet).delete()
        messages.success(request, "Successfully deleted {0}"
                         .format(supernet))
        return HttpResponseRedirect('/ipam')
    except:
        messages.error(request, "Error. Supernet doesn't exist.")
        return HttpResponseRedirect('/ipam/')


def view_subnet(request, subnet_id):
    return HttpResponse("Subnet ID: {}".format(subnet_id))


def new_subnet(request):
    supernets_list = SuperBlock.objects.all()
    if request.method == 'POST':
        form = NewSubNet(request.POST)
        address_space = form['address_space']
        vrf = form['vrf']
        route_target = form['route_target']
        vlan_id = form['vlan_id']
        environment = form['environment']
        region = form['region']
        customer_name = form['customer_name']
        super_block = SuperBlock.objects.get(id='32')
        try:
            new = Subnet(address_space = address_space,
                         vrf = vrf,
                         route_target = route_target,
                         vlan_id = vlan_id,
                         environment = environment,
                         region = region,
                         customer_name = customer_name,
                         super_block = super_block)
            new.save()
            messages.success(request, "{0} was successfully added."
                             .format(address_space))
        except:
            raise
            messages.error(request, "Error adding {0}."
                           .format(address_space))
            return HttpResponseRedirect('/ipam/subnet/new/')
        return HttpResponseRedirect('/ipam/')
    else:
        form = NewSubNet()
        return render(request, 'ipam/new_subnet.html',
                      {'form': form,
                       'supernets_list': supernets_list})
