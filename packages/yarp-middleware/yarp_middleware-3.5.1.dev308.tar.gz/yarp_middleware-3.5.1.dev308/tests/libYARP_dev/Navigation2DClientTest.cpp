/*
 * SPDX-FileCopyrightText: 2006-2021 Istituto Italiano di Tecnologia (IIT)
 * SPDX-License-Identifier: BSD-3-Clause
 */

#include <yarp/dev/INavigation2D.h>
#include <yarp/dev/IMap2D.h>
#include <yarp/dev/Map2DLocation.h>
#include <yarp/dev/Map2DArea.h>
#include <yarp/os/Network.h>
#include <yarp/os/LogStream.h>
#include <yarp/dev/PolyDriver.h>

#include <catch.hpp>
#include <harness.h>

#include "INavigation2DTest.h"

using namespace yarp::dev;
using namespace yarp::dev::Nav2D;
using namespace yarp::sig;
using namespace yarp::os;

TEST_CASE("dev::Navigation2DClientTest", "[yarp::dev]")
{
    YARP_REQUIRE_PLUGIN("map2DServer", "device");
    YARP_REQUIRE_PLUGIN("map2DClient", "device");
    YARP_REQUIRE_PLUGIN("localization2DServer", "device");
    YARP_REQUIRE_PLUGIN("fakeLocalizer", "device");
    YARP_REQUIRE_PLUGIN("navigation2DServer", "device");
    YARP_REQUIRE_PLUGIN("fakeNavigation", "device");
    YARP_REQUIRE_PLUGIN("navigation2DClient", "device");

    Network::setLocalMode(true);

    SECTION("Checking navigation2DClient < -> navigation2DServer communication and yarp::dev::Nav2D::INavigation2D methods")
    {
        PolyDriver ddnavserver;
        PolyDriver ddmapserver;
        PolyDriver ddmapclient;
        PolyDriver ddlocserver;
        PolyDriver ddnavclient;
        INavigation2D* inav = nullptr;
        IMap2D* imap = nullptr;

        ////////"Checking opening navigation2DServer and navigation2DClient polydrivers"
        {
            Property pmapserver_cfg;
            pmapserver_cfg.put("device", "map2DServer");
            REQUIRE(ddmapserver.open(pmapserver_cfg));

            Property pmapclient_cfg;
            pmapclient_cfg.put("device", "map2DClient");
            pmapclient_cfg.put("local", "/mapClientTest");
            pmapclient_cfg.put("remote", "/mapServer");
            REQUIRE(ddmapclient.open(pmapclient_cfg));
            REQUIRE(ddmapclient.view(imap));

            Property plocserver_cfg;
            plocserver_cfg.put("device", "localization2DServer");
            plocserver_cfg.put("subdevice", "fakeLocalizer");
            REQUIRE(ddlocserver.open(plocserver_cfg));

            Property pnavserver_cfg;
            pnavserver_cfg.put("device", "navigation2DServer");
            pnavserver_cfg.put("subdevice", "fakeNavigation");
            REQUIRE(ddnavserver.open(pnavserver_cfg));

            Property pnavclient_cfg;
            pnavclient_cfg.put("device", "navigation2DClient");
            pnavclient_cfg.put("local", "/navigationClientTest");
            pnavclient_cfg.put("navigation_server", "/navigationServer");
            pnavclient_cfg.put("map_locations_server", "/mapServer");
            pnavclient_cfg.put("localization_server", "/localizationServer");
            REQUIRE(ddnavclient.open(pnavclient_cfg));
            REQUIRE(ddnavclient.view(inav));
        }

        // Do tests
        exec_iNav2D_test_1(inav, imap);
        exec_iNav2D_test_2(inav, imap);

        //"Close all polydrivers and check"
        {
            CHECK(ddnavclient.close());
            CHECK(ddnavserver.close());
            CHECK(ddlocserver.close());
            CHECK(ddmapclient.close());
            CHECK(ddmapserver.close());
        }
    }

    Network::setLocalMode(false);
}
